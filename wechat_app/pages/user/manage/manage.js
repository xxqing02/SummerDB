Page({
    data: {
        username     : '',
        selectedType : '',
        license_plate: '',
        ident_number : '',
        vehicles     : [],
        isModalOpen  : false,
        Types        : ['小型车', '微型车', '紧凑车型', '中等车型','高级车型','豪华车型','三厢车型','CDV','MPV','SUV'],  
    },

    onLoad: function(options) 
    {
        this.username = wx.getStorageSync('username');
        this.fetchVehicleData();
    },

    onShow:function(options) {
        //console.log( this.getTabBar() + 'home');
        this.getTabBar().updateTabs(); 
        if (typeof this.getTabBar === 'function' &&
            this.getTabBar()) {
            this.getTabBar().setData({
                selected: 1
            })
        }
    },

    fetchVehicleData: function() 
    {
        var that = this;
        wx.request({
            url: 'https://app6321.acapp.acwing.com.cn/user_managecar/', 
            method: 'GET',
            data: {
                username: that.username,
                action  : 'inquire',
            },
            success: function(res) {
                that.setData({
                    vehicles: res.data
                });
            }
        })
    },

    openModal: function() 
    {
        this.setData({ 
            isModalOpen  : true,
            selectedType : '',   
            license_plate: '', 
            ident_number : '',
        });
    },
    closeModal: function() 
    {
        this.setData({ isModalOpen: false });
    },
    pickerChange: function(e) 
    {
        this.setData({
            selectedType: this.data.Types[e.detail.value]
        });
    },


    submitForm: function(e) 
    {
        var that = this;
        const { type, license_plate, ident_number } = e.detail.value;
        
        if (!type || !license_plate || !ident_number) {
            wx.showToast({
              title: '请填写所有字段',
              icon: 'none'
            });
            return;
        }

        var selectedType = this.data.Types[type];

        this.data.vehicles.push({ selectedType, license_plate, ident_number });
        this.setData({
            vehicles: this.data.vehicles
        });

        wx.request({
            url: 'https://app6321.acapp.acwing.com.cn/user_managecar/', 
            method: 'GET',
            data: {
                type         : selectedType,
                license_plate: license_plate,
                ident_number : ident_number,
                username     : this.username,
                action       :'add',
            },
            success: function(res) 
            {
                if (res.data.status === 'success') 
                {
                    wx.showToast({
                        title: '添加成功',
                        icon : 'success'
                    });

                    that.setData({ 
                        isModalOpen  : false,
                        selectedType : '',
                        license_plate: '',
                        ident_number : '',
                    });
                }
            }
        })
    },

    
    deleteVehicle: function(e) 
    {
        const ident_number = e.currentTarget.dataset.ident_number;
        
        const update = this.data.vehicles.filter(v => v.ident_number !== ident_number);
        this.setData({
            vehicles:update
        });

        wx.request({
            url: 'https://app6321.acapp.acwing.com.cn/user_managecar/', 
            method: 'GET',
            data: {
                ident_number: ident_number,
                action      : 'delete'
            },
            success: function(res) 
            {
                if (res.data.status === 'success') 
                {
                    wx.showToast({
                        title: '删除成功',
                        icon : 'success'
                    });
                }
            }
        })
    }
    
  });
  