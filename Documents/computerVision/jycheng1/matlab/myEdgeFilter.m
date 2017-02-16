function [Im] = myEdgeFilter(img, sigma)
  hsize = 2 * ceil(3*sigma) + 1;
  gFilter = fspecial('gaussian',hsize,sigma);
  ImgSmooth = myImageFilter(img, gFilter);
  Iy = myImageFilter(ImgSmooth, fspecial('sobel'));
  Ix = myImageFilter(ImgSmooth, fspecial('sobel')');
  [rows, cols] = size(ImgSmooth);
  
  ImUpdate = zeros(rows,cols);
  
  Im = zeros(rows,cols);

  findMag = @(x,y) sqrt((Ix(x,y)).^ 2 + (Iy(x,y)).^ 2);
  
  % regular edge detection
   for a = 1: 1: rows
       for b = 1: 1: cols
           ImUpdate(a,b) = findMag(a,b);
       end
   end
   
   imgPad = padarray(ImUpdate,[1,1]);
 
  % nms
  for a = 2: 1: (rows+1)
      for b = 2: 1: (cols+1)
          gradDir = radtodeg(atan(Iy(a-1,b-1)/Ix(a-1,b-1)));
          gradAngle = mod(round(gradDir/45),4) * 45;
          centerMag = imgPad(a,b);
          
          if gradAngle == 0
              n1Mag = imgPad(a,b-1);
              n2Mag = imgPad(a,b+1);
          elseif gradAngle == 45
              n1Mag = imgPad(a-1,b+1);
              n2Mag = imgPad(a+1,b-1);
          elseif gradAngle == 90
              n1Mag = imgPad(a-1,b);
              n2Mag = imgPad(a+1,b);    
          else %gradAngle == 135
              n1Mag = imgPad(a-1,b-1);
              n2Mag = imgPad(a+1,b+1);   
          end
          
          if (n1Mag > centerMag) || (n2Mag > centerMag)
              Im(a-1,b-1) = 0;
          else
              Im(a-1,b-1) = centerMag;
          end
          
      end
  end
  Im = Im/max(Im(:));
end
    
                
        
        
