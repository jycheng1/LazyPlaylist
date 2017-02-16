function [H, rhoScale, thetaScale] = myHoughTransform(Im, threshold, rhoRes, thetaRes)
    [maxY, maxX] = size(Im);
    maxRho = sqrt(maxY^2 + maxX^2);
    hRho = floor(maxRho/rhoRes) + 1;
    hTheta = floor((2*pi)/thetaRes) + 1;
	H = zeros(hRho,hTheta);
    
    rhoScale = 0:rhoRes:maxRho;
    thetaScale = 0:thetaRes:2*pi;
    
    for r = 1:maxY
        for c = 1:maxX
            if (Im(r,c) > threshold)
                for j = 1:hTheta 
                    rho = c * cos(thetaScale(j)) + r * sin(thetaScale(j));
                    if (rho > 0)
                        [~, i] = min(abs(rhoScale-rho));
                        H(i,j) = H(i,j) + 1;
                    end
                end
            end
        end
    end
    H = H/max(H(:));
    
end
        
        