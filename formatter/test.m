function [minS, s] = computeS(Ap, y, P)
       sP = inv(Ap' * Ap) * Ap' * y;
       s = P;
       iii = 0;

       for ii = 1:length(P)

              if P(ii)
                     iii++;
                     s(ii) = sP(iii);
              end

       end

       minS = min(sP);
end
