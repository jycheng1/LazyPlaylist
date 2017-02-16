function [rhos, thetas] = myHoughLines(H, nLines)
    imgPad = padarray(H,[1,1]);
    rhos = zeros(nLines,1);
    thetas = zeros(nLines,1);
    
    %nms
    
    for e = 1:nLines
        [~,idx]=max(imgPad(:));
        [a,b] = ind2sub(size(imgPad),idx);
        imgPad(a,b) = 0;
        imgPad(a,b-1) = 0;
        imgPad(a,b+1) = 0;
        imgPad(a-1,b+1) = 0;
        imgPad(a+1,b-1) = 0;
        imgPad(a-1,b) = 0;
        imgPad(a+1,b) = 0;
        imgPad(a-1,b-1) = 0;
        imgPad(a+1,b+1) = 0;
        rhos(e) = a-1;
        thetas(e) = b-1;
    end

end
        