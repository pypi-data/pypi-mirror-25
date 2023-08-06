from ruamel.yaml.comments import CommentedSeq, CommentedMap
from strictyaml.exceptions import YAMLValidationError
from strictyaml.exceptions import raise_exception
from strictyaml.representation import YAML
import sys

if sys.version_info[0] == 3:
    unicode = str


class Optional(object):
    def __init__(self, key):
        self.key = key

    def __repr__(self):
        return u'Optional("{0}")'.format(self.key)


class Validator(object):
    def __or__(self, other):
        return OrValidator(self, other)

    def __call__(self, chunk):
        return self.validate(chunk)


class OrValidator(Validator):
    def __init__(self, validator_a, validator_b):
        self._validator_a = validator_a
        self._validator_b = validator_b

    def validate(self, chunk):
        try:
            return self._validator_a(chunk)
        except YAMLValidationError:
            return self._validator_b(chunk)

    def __repr__(self):
        return u"{0} | {1}".format(repr(self._validator_a), repr(self._validator_b))


class MapPattern(Validator):
    def __init__(self, key_validator, value_validator):
        self._key_validator = key_validator
        self._value_validator = value_validator

    def validate(self, chunk):
        return_snippet = chunk.contentcopy()

        if not isinstance(return_snippet, CommentedMap):
            raise_exception(
                "when expecting a mapping",
                "found non-mapping",
                chunk,
            )
        else:
            for key, value in chunk.contents.items():
                valid_key = self._key_validator(chunk.key(key))
                valid_val = self._value_validator(chunk.val(key))
                return_snippet[valid_key] = valid_val

                del return_snippet[valid_key]
                return_snippet[valid_key] = self._value_validator(
                    chunk.val(key)
                )

        return YAML(return_snippet, chunk=chunk, validator=self)

    def __repr__(self):
        return u"MapPattern({0}, {1})".format(
            repr(self._key_validator), repr(self._value_validator)
        )


class Map(Validator):
    def __init__(self, validator):
        self._validator = validator

        self._validator_dict = {
            key.key if isinstance(key, Optional) else key: value for key, value in validator.items()
        }

        self._required_keys = [key for key in validator.keys() if not isinstance(key, Optional)]

    def __repr__(self):
        return u"Map({{{0}}})".format(', '.join([
            '{0}: {1}'.format(
                repr(key),
                repr(value),
            ) for key, value in self._validator.items()
        ]))

    def validate(self, chunk):
        return_snippet = chunk.contentcopy()

        if type(chunk.contents) != CommentedMap:
            raise_exception(
                "when expecting a mapping",
                "found non-mapping",
                chunk,
            )
        else:
            found_keys = set()
            for key, value in chunk.contents.items():
                if key not in self._validator_dict.keys():
                    raise_exception(
                        u"while parsing a mapping",
                        u"unexpected key not in schema '{0}'".format(unicode(key)),
                        chunk.key(key)
                    )

                found_keys.add(key)
                validator = self._validator_dict[key]
                del return_snippet[key]
                return_snippet[
                    YAML(key, chunk=chunk.key(key), validator=validator)
                ] = validator(chunk.val(key))

            if not set(self._required_keys).issubset(found_keys):
                raise_exception(
                    u"while parsing a mapping",
                    u"required key(s) '{0}' not found".format(
                        "', '".join(sorted(list(set(self._required_keys).difference(found_keys))))
                    ),
                    chunk,
                )

        return YAML(return_snippet, chunk=chunk, validator=self)


class Seq(Validator):
    def __init__(self, validator):
        self._validator = validator

    def __repr__(self):
        return "Seq({0})".format(repr(self._validator))

    def validate(self, chunk):
        return_snippet = chunk.contentcopy()

        if not isinstance(return_snippet, CommentedSeq):
            raise_exception(
                "when expecting a sequence",
                "found non-sequence",
                chunk,
            )
        else:
            for i, item in enumerate(chunk.contents):
                return_snippet[i] = self._validator(chunk.index(i))

        return YAML(return_snippet, chunk=chunk, validator=self)


class FixedSeq(Validator):
    def __init__(self, validators):
        self._validators = validators

    def __repr__(self):
        return "FixedSeq({0})".format(repr(self._validators))

    def validate(self, chunk):
        return_snippet = chunk.contentcopy()

        if not isinstance(return_snippet, CommentedSeq):
            raise_exception(
                "when expecting a sequence of {0} elements".format(len(self._validators)),
                "found non-sequence",
                chunk,
            )
        else:
            if len(self._validators) != len(chunk.contents):
                raise_exception(
                    "when expecting a sequence of {0} elements".format(len(self._validators)),
                    "found a sequence of {0} elements".format(len(chunk.contents)),
                    chunk,
                )
            for i, item_and_val in enumerate(zip(chunk.contents, self._validators)):
                item, validator = item_and_val
                return_snippet[i] = validator(chunk.index(i))

        return YAML(return_snippet, chunk=chunk, validator=self)


class UniqueSeq(Validator):
    def __init__(self, validator):
        self._validator = validator

    def __repr__(self):
        return "UniqueSeq({0})".format(repr(self._validator))

    def validate(self, chunk):
        return_snippet = chunk.contentcopy()

        if type(chunk.contents) != CommentedSeq:
            raise_exception(
                "when expecting a unique sequence",
                "found non-sequence",
                chunk,
            )
        else:
            existing_items = set()

            for i, item in enumerate(chunk.contents):
                if item in existing_items:
                    raise_exception(
                        "while parsing a sequence",
                        "duplicate found",
                        chunk
                    )
                else:
                    existing_items.add(item)
                    return_snippet[i] = self._validator(chunk.index(i))

        return YAML(return_snippet, chunk=chunk, validator=self)
