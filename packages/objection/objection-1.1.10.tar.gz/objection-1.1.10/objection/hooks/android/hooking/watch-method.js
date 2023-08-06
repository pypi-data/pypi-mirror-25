// Watches a Java class method and reports on invocations.
// All of the matching overloads of the method in question
// is also watched.

var Throwable = Java.use('java.lang.Throwable');

var target_class = Java.use('{{ target_class }}');
var overload_count = eval('target_class.{{ target_method }}.overloads.length');

send(JSON.stringify({
    status: 'success',
    error_reason: NaN,
    type: 'watch-class-method',
    data: 'Found class with ' + overload_count + ' overloads for {{ target_method }}'
}));

// Hook all of the overloads found for this class.method
for (var i = 0; i < overload_count; i++) {

    send(JSON.stringify({
        status: 'success',
        error_reason: NaN,
        type: 'watch-class-method',
        data: 'Hooking overload ' + (i + 1)
    }));

    // Hook the overload.
    eval('target_class.{{ target_method }}.overloads[i]').implementation = function () {

        var message = 'Called {{ target_class }}.{{ target_method }} (args: ' + arguments.length + ')';

        // if we should include a backtrace to here, do that.
        if ('{{ include_backtrace }}' == 'True') {

            message += '\nBacktrace:\n\t' + Throwable.$new().getStackTrace()
                .map(function (stack_trace_element) {

                    return stack_trace_element.toString() + '\n\t';
                }).join('');
        }

        send(JSON.stringify({
            status: 'success',
            error_reason: NaN,
            type: 'watch-class-method',
            data: message
        }));

        // continue with the original method
        eval('this.{{ target_method }}.apply(this, arguments)');
    }
}
