Page({
    data  :{
        userType : 'repairman',
    },
    onLoad: function(options) 
    {
        this.username = wx.getStorageSync('username');
        this.setData({
            username: this.username
        });
    },
    
    onShow:function(options) {
        console.log( this.getTabBar() + 'home');
        this.getTabBar().updateTabs(); 
        if (typeof this.getTabBar === 'function' &&
            this.getTabBar()) {
            this.getTabBar().setData({
                selected: 1
            })
        }
    }
});