import util.*
% ADD CORRECT INDENTATION
function foo = myFun(a, b, c)
    % ADD SPACES BETWEEN EXPRESSIONS

    if a == '{' || a == '[' % bla
        N = norm(a .* b - c)
        % REMOVE ADDITIONAL SPACES
        foo = -N * a(3) / N
        % TREAT POWERS AND RATIONAL NUMBERS AND NEGATIVES AS SINGLE EXPRESSION ιω ϱϱκφ
        p = foo ^ N - 17
        r = 42/0.8e15
        d += 4.7e11
        neg = -r
    end

    try something; catch e; end; % bla

    for k = 1:N
        % ADD INDENTATION AFTER LINE BREAK
        k++

        t = a * k ...
            +b .* k ^ 2 ... % comment
            +c * k ^ 3
        vectorofstrings = ['α' 'β' 'γ'];
        vectorofstrings = ['α', 'β', 'γ'];
        vectorofstuff = ['foo' dead('beef', 3.14, bar) -foo('bar', '42')]

        if (norm(t)) % ADD NEWLINE BEFORE AND AFTER BLOCK
            fprintf('Hello world \n');
        end;

    end

    % INDENT MATRICES SPLIT OVER MULTIPLE LINES
    M = [1 -2 3;
        4 5 -6;
        -7 8 9] % REMOVE ADDITIONAL NEWLINES

    % exclude the next N (default=1) nonempty lines of code from formatting
    % formatter ignore N    code)
    this=a   *very*  ill ^ formated+    loc

    C = {1
        [2 3]'
        {1 M 'three'}};

end
