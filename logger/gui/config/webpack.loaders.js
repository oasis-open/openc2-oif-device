import { images } from 'min-document';
import path from 'path';

export const commonImages = /\.(?:bmp|ico|gif|png|jpe?g|tiff|webp)$/;

const file_loader = {
  loader: 'file-loader',
  options: {
    name: (rPath, rQuery) => {
      const ext = path.extname(rPath);
      if (commonImages.test(ext)) {
        return 'img/[name].[ext]';
      }
      return 'assets/[ext]/[name].[ext]'
    }
  }
};

export default {
  css: {
    loader: 'css-loader',
    options: {
      url: false
    }
  },
  file: file_loader,
  less: {
    loader: 'less-loader',
    options: {
      lessOptions: {
        strictMath: true
      }
    }
  },
  url: {
    loader: 'url-loader',
    options: {
      limit: 10 * 1024,
      fallback: file_loader
    }
  }
};