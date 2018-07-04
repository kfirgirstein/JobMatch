app.utils = function ($scope, $timeout) {
    $scope.closeModal = function (id) {
        $("#" + id).modal("hide");
    }
    $scope.safeApply = function (fn) {
        var phase = this.$root.$$phase;
        if (phase == '$apply' || phase == '$digest') {
            if (fn && (typeof (fn) === 'function')) {
                fn();
            }
        } else {
            this.$apply(fn);
        }
    };

};




/////////////////////////////// utils /////////////////////////////////////
// convert array of objects to dictionary
Array.prototype.ToDict = function (key, val) {
    var o = {};
    for (i = 0; i < this.length; i++) {
        o[this[i][key]] = this[i][val];
    }
    return o;
}
// shorthand by first-last characters
String.prototype.ToFL = function () {
    return this[0] + this[this.length - 1];
}
