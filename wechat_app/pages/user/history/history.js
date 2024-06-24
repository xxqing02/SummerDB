// pages/user/history/history.js
Page({

  data: {
    
    username:"",
    history :[],
    statusBarHeight: wx.getStorageSync('statusBarHeight'),
    navigationBarHeight: wx.getStorageSync('navigationBarHeight'),
    menuButtonHeight: wx.getStorageSync('menuButtonHeight'),
    navigationBarAndStatusBarHeight:
            wx.getStorageSync('statusBarHeight') +
            wx.getStorageSync('navigationBarHeight'),
  },

  onLoad(options) {
    this.username = wx.getStorageSync('username');
    this.fetchHistory();
  },

  onShow() {

  },
  
  fetchHistory: function() {
    var that = this;
    wx.request({
        url    : 'https://app6321.acapp.acwing.com.cn/user_commissionhistory/',
        method : 'GET',
        data   : {
            username: that.username,
        },
        success: function(res) {
            that.setData({
                history: res.data
            });
        }
    });
},

  goBack: function() {
    wx.navigateBack({
      delta: 1 
    });
  }

})