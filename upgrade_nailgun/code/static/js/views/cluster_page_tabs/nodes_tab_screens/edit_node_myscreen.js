/*
 * Copyright 2013 Mirantis, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
**/
define(
[
    'underscore',
    'utils',
    'models',
    'views/cluster_page_tabs/nodes_tab_screens/myscreen'
],
function(_, utils, models, Screen) {
    'use strict';
    var EditNodeScreen;

    EditNodeScreen = Screen.extend({
        constructorName: 'EditNodeScreen',
        keepScrollPosition: true,
        disableControls: function(disable) {
            this.updateButtonsState(disable || this.isLocked());
        },
        returnToNodeList: function() {
           this.goToNodeList();
        },
        initialize: function(options) {
            _.defaults(this, options);
            this.nodes=options.model;
            //console.log(this.nodes);
        }
    });

    return EditNodeScreen;
});
