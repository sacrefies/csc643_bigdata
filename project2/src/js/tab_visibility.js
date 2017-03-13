// Copyright 2017 team1@course_bigdata, Saint Joseph's University
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

var getNavTabId = function (name) {
    return "#nav" + name;
};

var getTabContentId = function (name) {
    return "#tab" + name;
};

var switchTab = function (name) {
    if (!name) name = "QueryA";
    // alert(name);
    var navTabId = getNavTabId(name);
    var tabContentId = getTabContentId(name);

    // set all nav tab items deactivated first
    // var li = $("#navControl li");
    // for (var i = 0; i < li.length; i++) {
    //     console.log(li[i].className);
    //     li[i].className = "";
    // }
    $("#navControl li").each(function () {
        $(this).removeClass();
    });
    // set the nav tab activated
    $(navTabId).attr("class", "active");
    // set all tabs deactivated first
    $(".tab-pane").each(function () {
        $(this).attr("class", "tab-pane fade");
    });
    $(tabContentId).addClass("in");
    $(tabContentId).addClass("active");
};
