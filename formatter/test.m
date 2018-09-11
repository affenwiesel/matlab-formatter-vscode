function test = myFun(a, b, c)

    parfor i = 1:100

        test = a * i + b * i^2 + c * i^3;
    end

    if condition
        condition
    end

end
