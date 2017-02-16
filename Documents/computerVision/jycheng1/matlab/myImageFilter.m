function [img1] = myImageFilter(img0, h)
  padSize = floor((size(h,1) / 2));
  imgPad = padarray(img0,[padSize, padSize], 'replicate');
  [rows, cols] = size(img0);
  img1 = zeros(rows,cols);
  for a = padSize + 1: 1: (rows+padSize)
      for b = padSize + 1: 1: (cols+padSize)
          C = imgPad((a-padSize):(a + padSize),(b - padSize):(b + padSize));
          C = C .* h;
          img1(a - padSize,b - padSize) = sum(sum(C));
      end
  end
end
