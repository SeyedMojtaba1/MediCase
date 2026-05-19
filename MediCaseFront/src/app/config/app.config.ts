// ------------------------------
// App Config - Central Configuration
// ------------------------------

export interface ThemeConfig {
  colors: {
    primary: string;
    secondary: string;
    success: string;
    warning: string;
    danger: string;
    info: string;
    textLight: string;
    textDark: string;
    backgroundGradient: string;
  };
}

export interface AppConfig {
  baseURL: string; // آدرس API
  theme: ThemeConfig; // رنگ و فونت
  timeout?: number; // اختیاری، مثلا HTTP timeout
  logoURL?: string; // URL لوگوی سایت
  olomURL?: string;

  [key: string]: any; // برای مقادیر اضافه در آینده
}

// ------------------------------
// نمونه مقدار اولیه
// می‌تونی رنگ‌ها و فونت‌ها رو بعدا تغییر بدی
// ------------------------------
export const APP_CONFIG: AppConfig = {
<<<<<<< HEAD
  baseURL: 'https://medicase-isfahan.ir/api/',
=======
  baseURL: 'https://medicase-isfahan.ir/',
>>>>>>> FrontEnd
  timeout: 5000,
  logoURL: 'images/logo/medicase.png',
  olomURL: 'images/logo/olom.png',
  theme: {
    colors: {
      primary: '#148591', // رنگ متن و دکمه های اکتیو
      secondary: '#DAEAEA', // پس زمینه باکس ها
      success: '#D6E4D5', // وضعیت موفقیت
      warning: '#FFC107', // هشدار (اختیاری)
      danger: '#FF4D4F', // خطا (اختیاری)
      info: '#C6C7E5', // رنگ ثانویه
      textLight: '#FFFFFF', // متن سفید
      textDark: '#000000', // متن سیاه
      backgroundGradient:
        'linear-gradient(to right, #C6C7E5, #DAEAEA 50%, #C6C7E5)',
    },
  },
};
