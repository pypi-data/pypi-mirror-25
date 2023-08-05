# Copyright 2017 Mycroft AI, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from xxhash import xxh32


def lines_hash(lines):
    """
    Creates a unique binary id for the given lines
    Args:
        lines (list<str>): List of strings that should be collectively hashed
    Returns:
        bytearray: Binary hash
    """
    x = xxh32()
    for i in lines:
        x.update(i.encode())
    return x.digest()


def tokenize(sentence):
    """
    Converts a single sentence into a list of individual significant units
    Args:
        sentence (str): Input string ie. 'This is a sentence.'
    Returns:
        list<str>: List of tokens ie. ['this', 'is', 'a', 'sentence']
    """
    tokens = []

    class Vars:
        last_pos = -1

    def update(c, i):
        if c.isalpha() or c in '-{}':
            if Vars.last_pos < 0:
                Vars.last_pos = i
        else:
            if Vars.last_pos >= 0:
                tokens.append(sentence[Vars.last_pos:i].lower())
            if not c.isspace() and c not in '.!?':
                tokens.append(c)
            Vars.last_pos = -1

    for i, char in enumerate(sentence):
        update(char, i)
    update(' ', len(sentence))
    return tokens


def expand_parentheses(sent):
    """
    ['1', '(', '2', '|', '3, ')'] -> [['1', '2'], ['1', '3']]
    For example:

    Will it (rain|pour) (today|tomorrow|)?

    ---->

    Will it rain today?
    Will it rain tomorrow?
    Will it rain?
    Will it pour today?
    Will it pour tomorrow?
    Will it pour?

    Args:
        sent (list<str>): List of tokens in sentence
    Returns:
        list<list<str>>: Multiple possible sentences from original
    """
    if '(' not in sent or '|' not in sent:
        return [sent]
    else:
        class State:  # Parentheses state
            IN = 0
            OUT = 1
        state = State.OUT
        all_pars = {}
        par_groups = []
        cur_group = []

        remaining = []

        for token in sent:
            if state == State.IN:
                if token in ')|':
                    par_groups.append(cur_group)
                    cur_group = []
                else:
                    cur_group.append(token)
                if token == ')':
                    state = State.OUT
                    all_pars[len(remaining)] = par_groups
                    remaining.append('()')
                    par_groups = []
            elif state == State.OUT:
                if token == '(':
                    state = State.IN
                else:
                    remaining.append(token)

        sents = [[]]
        for i, token in enumerate(remaining):
            if token == '()':
                for j in list(range(len(sents))):
                    pairs = all_pars[i]
                    for p in pairs[1:]:
                        sents.append(sents[j] + p)
                    sents[j] += pairs[0]
            else:
                for sent in sents:
                    sent.append(token)
        return sents


def resolve_conflicts(inputs, outputs):
    """
    Checks for duplicate inputs and if there are any,
    remove one and set the output to the max of the two outputs
    Args:
        inputs (list<list<float>>): Array of input vectors
        outputs (list<list<float>>): Array of output vectors
    Returns:
        tuple<inputs, outputs>: The modified inputs and outputs
    """
    new_in, new_out = [], []
    for i, inp in enumerate(inputs):
        found_duplicate = False
        for j in range(i + 1, len(inputs)):
            if inp == inputs[j]:
                found_duplicate = True
                if outputs[i] > outputs[j]:
                    outputs[j] = outputs[i]
        if not found_duplicate:
            new_in.append(inputs[i])
            new_out.append(outputs[i])
    return new_in, new_out


class StrEnum(object):
    """Enum with strings as keys. Implements items method"""
    @classmethod
    def values(cls):
        return [getattr(cls, i) for i in dir(cls) if not i.startswith("__") and i != 'values']
