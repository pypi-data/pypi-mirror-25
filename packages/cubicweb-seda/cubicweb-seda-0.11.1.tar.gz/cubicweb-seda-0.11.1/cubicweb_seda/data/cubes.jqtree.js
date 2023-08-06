// copyright 2016-2017 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
// contact http://www.logilab.fr -- mailto:contact@logilab.fr
//
// This program is free software: you can redistribute it and/or modify it under
// the terms of the GNU Lesser General Public License as published by the Free
// Software Foundation, either version 2.1 of the License, or (at your option)
// any later version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
// details.
//
// You should have received a copy of the GNU Lesser General Public License along
// with this program. If not, see <http://www.gnu.org/licenses/>.


jqtree = {
    jqTree: function(domid, dragAndDrop) {
        var $tree = cw.jqNode(domid);
        // tree display and basic controls.
        $tree.tree({
            dragAndDrop: dragAndDrop,
            autoOpen: 0,  // only open level-0
            selectable: false,
            autoEscape: false,
            closedIcon: $('<i class="glyphicon glyphicon-expand"></i>'),
            openedIcon: $('<i class="glyphicon glyphicon-collapse-down"></i>'),
            onCanMove: function(node) {
                return node.maybeMoved;
            },
            onCanMoveTo: function(moved_node, target_node, position) {
                if ( target_node.id === undefined ) {
                    return false;
                } else if ( position != 'inside' ) {
                    // moving before/after is not supported
                    return false;
                } else {
                    // avoid moving into the same parent
                    function isMovedNode(element, index, array) {
                        return element.id == moved_node.id;
                    }
                    if ( target_node.children.some(isMovedNode) ) {
                        return false;
                    }
                    // ensure the new parent target accept the moved node
                    return target_node.maybeParentOf.indexOf(moved_node.type) !== -1;
                }
            },
            onCreateLi: function(node, $li) {
                $li.find('.jqtree-title').addClass(node.type);

                var selectedId = $tree.tree('getTree').children[0].selected;

                if ( selectedId !== null && node.id === selectedId ) {
                    // add "jqtreeNodeSelected" CSS class so that the current
                    // element in the tree gets highlighted.
                    $li.find('.jqtree-title').addClass('jqtreeNodeSelected');
                }
            }
        });
        // tree events bindings.
        $tree.bind(
            'tree.init',
            function() {
                var selectedId = $tree.tree('getTree').children[0].selected;
                var node = $tree.tree('getNodeById', selectedId);
                var parentNode = node.parent;
                while (parentNode !== null) {
                    $tree.tree('openNode', parentNode);
                    parentNode = parentNode.parent;
                }
            }
        );
        $tree.bind(
            'tree.move',
            function(event) {
                event.preventDefault();
                // do the move first, and then POST back.
                event.move_info.do_move();
                asyncRemoteExec('jqtree_reparent', event.move_info.moved_node.id,
                                event.move_info.target_node.id);
            }
        );
    }
};
