// components/custom-tab-bar/index.js
const app = getApp();

Component({
    data: {
        selected:0,
        tabs: [],
        repair: [
            {
            "pagePath": "pages/repair_man/work/work",
            "text": "管理",
            "iconPath": "/static/image/icon/qianshoushenpitongguo-xianxing.png",
            "selectedIconPath": "/static/image/icon/qianshoushenpitongguo.png"
            },

            {
            "pagePath": "pages/repair_man/home/home",
            "text": "我的",
            "iconPath": "/static/image/icon/hezuoguanxi-xianxing.png",
            "selectedIconPath": "/static/image/icon/hezuoguanxi.png"
            }
        ],
        user: [
            {
                "pagePath": "pages/user/inquire/inquire",
                "text": "查询",
                "iconPath": "/static/image/icon/sousuo-xianxing.png",
                "selectedIconPath": "/static/image/icon/sousuo.png"
            },
            {
                "pagePath": "pages/user/manage/manage",
                "text": "管理",
                "iconPath": "/static/image/icon/danju-xianxing.png",
                "selectedIconPath": "/static/image/icon/danju.png"
            },
            {
                "pagePath": "pages/user/home/home",
                "text": "我的",
                "iconPath": "/static/image/icon/hezuoguanxi-xianxing.png",
                "selectedIconPath": "/static/image/icon/hezuoguanxi.png"
            }
        ]
    },
    attached() {
    },
    methods: {
        switchTab(e) {
            const data = e.currentTarget.dataset
            const url = data.path
            //console.log(data.index,url);
            wx.switchTab({
                url: '/' + url,
            })
        },

        updateTabs() {
            const app = getApp();
            const userType = app.globalData.userType;
            console.log(userType);
            if (userType === 'repairman') {
                this.setData({ tabs: this.data.repair });
            } else {
                this.setData({ tabs: this.data.user });
            }
        }
    }
})