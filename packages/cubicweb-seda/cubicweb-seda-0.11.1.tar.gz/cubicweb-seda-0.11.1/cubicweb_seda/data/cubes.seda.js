// copyright 2015-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

seda = {
    toggleFormMetaVisibility: function(domid) {
        var $node = cw.jqNode(domid);
        $node.toggleClass('hidden');
        var $a = $node.parent().children('a');
        var classes = $a.attr('class').split(' ');
        var icon = classes[0];
        if (icon == 'icon-list-add') {
            classes[0] = 'icon-up-open';
        } else {
            classes[0] = 'icon-list-add';
        }
        $a.attr('class', classes.join(' '));
    },

};
