% ADD CORRECT INDENTATION
function foo = myFun(a, b, c)
    % ADD SPACES BETWEEN EXPRESSIONS
    N = norm(a .* b - c)
    % REMOVE ADDITIONAL SPACES
    foo = -N * a(3) / N
    % TREAT POWERS AND RATIONAL NUMBERS AND NEGATIVES AS SINGLE EXPRESSION ιω ϱϱκφ
    p = foo^N - 17
    r = 42/0.8e15
    d = 4.7e11
    neg = -r

    for k = 1:N
        % ADD INDENTATION AFTER LINE BREAK
        t = a * k ...
            + b .* k^2 ...
            + c * k^3

        if (norm(t))% ADD NEWLINE BEFORE AND AFTER BLOCK
            fprintf('t>0')
        end

    end

    % INDENT MATRICES SPLIT OVER MULTIPLE LINES
    M = [1 -2 3;
        4 5 -6;
        -7 8 9]% REMOVE ADDITIONAL NEWLINES

    even_more = code
end
