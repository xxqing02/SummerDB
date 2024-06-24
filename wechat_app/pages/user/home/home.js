Page({
    data:{
        username:"",
    },
    onLoad:function(){
        this.username = wx.getStorageSync('username');
        this.setData({
            username: this.username
        });
    },

    onShow:function(options) {
        this.getTabBar().updateTabs(); 
        if (typeof this.getTabBar === 'function' &&
            this.getTabBar()) {
            this.getTabBar().setData({
                selected: 2
            })
        }
    },
    navigateToHistory: function() {
        wx.navigateTo({
          url: '/pages/user/history/history' 
        });
      },
    navigateToMessage: function() {
        wx.navigateTo({
            url: '/pages/user/message/message'
        });
    }
});