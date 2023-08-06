# Copyright 2017- Robot Framework Foundation
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

from .repo import get_repository


LABELS = '''
bug             ee0701
enhancement     84b6eb
task            ededed

alpha 1         ffffff
alpha 2         ffffff
alpha 3         ffffff
beta 1          ffffff
beta 2          ffffff
beta 3          ffffff
rc 1            ffffff
rc 2            ffffff
rc 3            ffffff

bwic            fbca04
depr            fef2c0

duplicate       000000
wont fix        000000
invalid         000000
in progress     ededed
pending         ededed
help wanted     ededed
needs review    ededed

prio-critical   00441b
prio-high       006d2c
prio-medium     238b45
prio-low        41ae76
'''


def initialize_labels(repository, username=None, password=None):
    repository = get_repository(repository, username, password,
                                auth_required=True)
    labels = [label.rsplit(None, 1) for label in LABELS.splitlines() if label]
    existing_labels = {_normalize(label.name): label.name
                       for label in repository.get_labels()}
    for name, color in labels:
        try:
            normalized = existing_labels[_normalize(name)]
        except KeyError:
            repository.create_label(name, color)
        else:
            repository.get_label(normalized).edit(name, color)


def _normalize(label):
    return label.lower().replace(' ', '')
