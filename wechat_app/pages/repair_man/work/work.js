// pages/repairman/repairman.js
Page({
    data: {
        username : '',
        userType : 'repairman',
        tasks    : []
    },

    onLoad: function(options) 
    {
        this.username = wx.getStorageSync('username');  
    },

    onShow: function(){
        this.fetchTasks();
        console.log( this.getTabBar() + 'work');
        this.getTabBar().updateTabs(); 
        if (typeof this.getTabBar === 'function' &&
            this.getTabBar()) {
            this.getTabBar().setData({
                selected: 0
            })
        }
    },

    fetchTasks: function() 
    {
        var that = this;
        wx.request({
            url: 'https://app6321.acapp.acwing.com.cn/repair_getorder/',
            method: 'GET',
            data: { 
                username: that.username, 
            },
            success: function(res) 
            {
                that.setData({
                    tasks: res.data
                });
            }
        });
    },

    finishTask: function(e) 
    {
        let that=this;
        let taskId = e.currentTarget.dataset.id;
        wx.request({
            url: 'https://app6321.acapp.acwing.com.cn/repair_finish/',
            data: { 
                id: taskId 
            },
            method: 'GET',
            success: function(res) 
            {
                if (res.data.status === 'success') 
                {
                    wx.showToast({
                        title: '任务完成',
                        icon: 'success'
                    });

                    that.fetchTasks();
                }
            }
        });
    }
});
