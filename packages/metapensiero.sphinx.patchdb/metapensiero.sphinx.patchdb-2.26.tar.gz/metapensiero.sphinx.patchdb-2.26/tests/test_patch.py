# -*- coding: utf-8 -*-
# :Project:   PatchDB -- Patch tests
# :Created:   mer 24 feb 2016 16:44:43 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from __future__ import unicode_literals


def test_patch():
    from metapensiero.sphinx.patchdb.manager import patch_manager
    from metapensiero.sphinx.patchdb.patch import make_patch, parse_deps, DependencyError

    pm = patch_manager(None)
    first = make_patch('first', 'script',
                       dict(revision=1, language='test',
                            depends='second',
                            preceeds='third'))
    pm['first'] = first

    # __str__
    second = make_patch('second', 'script',
                        dict(revision=2, language='test'))
    pm['second'] = second
    print('%s' % second)
    assert str(second) == 'script "second@2"'

    third = make_patch('third', 'script',
                       dict(depends='second@1',
                            brings='second@2',
                            preceeds='fourth@2',
                            language='test'))
    pm['third'] = third
    assert str(third) == 'patch "third@1"'

    # adjustUnspecifiedRevisions
    first = pm['first']
    assert first.depends == [('second', None)]
    assert first.preceeds == [('third', None)]
    first.adjustUnspecifiedRevisions(pm)
    assert first.depends == [('second', 2)]
    assert first.preceeds == [('third', 1)]
    third = pm['third']
    assert third.preceeds == [('fourth', 2)]
    try:
      third.adjustUnspecifiedRevisions(pm)
    except DependencyError as e:
      assert 'patch "third@1"' in str(e) and 'preceeds "fourth@2"' in str(e)
    else:
      assert False, "should raise a DependencyError"

    # parse_deps
    assert parse_deps('patchid@10') == [('patchid', 10)]
    assert parse_deps('patchid@10, other') == [('other', None), ('patchid', 10)]
    assert parse_deps(' z, x , y@10 , a,c') == \
           [('a', None), ('c', None), ('x', None), ('y', 10), ('z', None)]
