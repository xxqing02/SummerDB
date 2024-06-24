// app.js
App({ 
    onLaunch:function() 
    {
        wx.clearStorageSync();
        this.getNavigationBarHeight();
    },

    getNavigationBarHeight(){
        const { statusBarHeight, platform } = wx.getSystemInfoSync()
        const { top, height } = wx.getMenuButtonBoundingClientRect()
    
        wx.setStorageSync('statusBarHeight', statusBarHeight)
        wx.setStorageSync('menuButtonHeight', height ? height : 32)
        
        if (top && top !== 0 && height && height !== 0) {
            const navigationBarHeight = (top - statusBarHeight) * 2 + height
            wx.setStorageSync('navigationBarHeight', navigationBarHeight)
        } else {
            wx.setStorageSync(
              'navigationBarHeight',
              platform === 'android' ? 48 : 40
            )
        }
    },
    
    globalData:
    {
        userType:null
    },
    
})