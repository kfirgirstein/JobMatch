/*
 *Author : kfir G.
 * Valid is : 48-57 or 96-105
 */
function isNumberKey(e) {
    var result = false;
    try {
        var charCode = (e.which) ? e.which : e.keyCode;
        if ((charCode >= 48 && charCode <= 57) || (charCode >= 96 && charCode <= 105 && e.key != 'e')) {
            result = true;
        }
    }
    catch (err) {
        console.log(err);
    }
    return result;
}
/*
 *Author : kfir G.
 * Valid is : 8-backspace, 9-Tab , 13-enter ,39-right arrow , 40-down arrow ,46-delete, 110- decimal point
 */
function isValidInput(e) {
    var result = false;
    try {
        var charCode = (e.which) ? e.which : e.keyCode;
        switch (charCode) {
            case 8: case 9: case 13: case 39: case 40: case 46: case 110:
                return true;
        }

    }
    catch (err) {
        console.log(err);
    }
    return result;
}




/*
 *Author : Raz C.
 * check for valid char in floating number input field
 */
function isNumberOrDecimal(e) {
    var result = false;
    try {
        var key = e.originalEvent.key;
        //special keys
        switch (key) {
            case ".": case "Tab": case "ArrowRight": case "ArrowLeft": case "ArrowDown": case "Delete": case "Backspace": result = true; break;
            default: break;
        }
        //number keys
        if (key >= "0" && key <= "9") {
            result = true;
        }
    }
    catch (err) {
        console.log(err);
    }
    return result;
}
// utils
function isObject(obj) {
    return obj !== null && typeof obj === 'object';
}


/*
 *Author : Raz C.
 * Directive for input float number
 */
app1.directive('validNumber', function ($parse) {
    return {
        restrict: 'A',
        link: function (Out_scope, elm, attrs) {

            scope: {
                prevInput = "";
                oldVal = null;
            }
            elm.on("keydown keyup", function (e) {

                if (!isNumberOrDecimal(e)) {
                    e.preventDefault();
                    return;
                }
                var input, value, length;


                input = e.originalEvent.key;
                length = elm[0].value.length;
                value = elm[0].value;
                // check if this is valid number with floating point
                if (((length == '0' || value.indexOf(".") > 0 || prevInput == '.') && input == '.')) {
                    e.preventDefault();
                }


                //update previous Input
                prevInput = input;


                //prevent about max
                if (Number(elm.val()) > Out_scope.UpdateNumberToEn(attrs.max) &&
                    e.keyCode != 46 // delete
                    &&
                    e.keyCode != 8 // backspace
                ) {
                    $('#MaxErrorMessageBuy').show();
                    $('#MaxErrorMessageSend').show();
                    e.preventDefault();
                    //elm.val(oldVal);
                    Out_scope.trAmount = oldVal;
                    Out_scope.safeApply();

                } else {
                    oldVal = Number(elm.val());
                }


            });

        }
    }
});


/*
* directive for input with copy button
*/
app1.directive('inputCopy', function ($compile) {

    return {
        scope: {
            bind: "=",
            inputId: "@"
        },
        template: `
            <div class="input-group input-group-sm mb-3">
            <input id={{inputId}} type="text" class="form-control" data-ng-model="bind" readonly style="padding:17px 20px;cursor:copy;background-color:#fff;">
            <div class="input-group-append">
            <button class="btn btn-primary" type="button" data-ng-click="CopyInputText(inputId)">Copy</button>
            </div></div>`,

        link: function (scope) {
            scope.CopyInputText = function (item) {
                $('#' + item + '').select();
                document.execCommand('copy');
            };
        }
    };




    //$(window).on('resize', function () {
    //    var win = $(this);
    //    if (win.width() < 576) {

    //    }
    //});




});
