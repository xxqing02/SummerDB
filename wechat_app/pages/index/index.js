// index.js
Page({
    onLoad: function () {
      setTimeout(() => {
        wx.redirectTo({
          url: '/pages/login/login'
        });
      }, 2000);  
    }
});