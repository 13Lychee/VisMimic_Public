<template>
    <div class="container">
        <div class="header">
            <div class="title">Media View</div>
            <div class="help">
                <!-- <img src="@/assets/image 578.png" alt="help" height="100%"> -->
                <img src="@/assets/media_info.png" alt="help" height="100%">
            </div>
        </div>

        <div class="content-container">
            <div class="content">
                <div class="nav">
                    <div class="upload">
                        Upload
                    </div>
                    <div class="select">
                        <label for="sportOptions">
                            Select Sport:
                        </label>
                        <select id="sportOptions" v-model="selectedOption" class="selection-box">
                            <option value="Squat">Sumo Squat</option>
                            <option value="saab">Saab</option>
                            <option value="mercedes">Mercedes</option>
                            <option value="audi">Audi</option>
                        </select>
                    </div>
                </div>
                <div class="media-container">
                    <div class="video-wrapper">
                        <!-- 视频播放器的白色框和文本标识 -->
                        <!-- <div class="label-box">
                            Preview
                        </div> -->
                        <video v-if="currentVideo" :src="currentVideo" controls></video>
                    </div>
                </div>
                <div class="operation-container">
                    <div class="update-ori" :style="getBackgroundColor('ori')">
                        <div class="upload-icon" @click="handleUploadClick('ori')">
                            <!-- 上传图标 ori 的白色框和文本标识 -->
                            <div class="label-box">
                                Ori.
                            </div>
                            <img v-if="oriVideoCover" :src="oriVideoCover" alt="ori video cover" height="100%" class="video-cover">
                            <!-- <img v-else src="@/assets/image 49.png" alt="upload" height="100%" class="upload-icon-img"> -->
                            <img v-else src="@/assets/media_upload.png" alt="upload" height="100%" class="upload-icon-img">
                            <!-- <img src="@/assets/image 49.png" alt="upload" height="100%"> -->
                            <!-- 隐藏的文件输入框 -->
                            <input type="file" ref="oriInput" accept="video/*" style="display: none;" @change="handleFileChange('ori', $event)">
                        </div>
                    </div>
                    <div class="update-ref" :style="getBackgroundColor('ref')">
                        <div class="upload-icon" @click="handleUploadClick('ref')">
                            <!-- 上传图标 ref 的白色框和文本标识 -->
                            <div class="label-box">
                                Ref.
                            </div>
                            <img v-if="refVideoCover" :src="refVideoCover" alt="ref video cover" height="100%" class="video-cover">
                            <!-- <img v-else src="@/assets/image 49.png" alt="upload" height="100%" class="upload-icon-img"> -->
                            <img v-else src="@/assets/media_upload.png" alt="upload" height="100%" class="upload-icon-img">
                            <!-- <img src="@/assets/image 49.png" alt="upload" height="100%"> -->
                            <!-- 隐藏的文件输入框 -->
                            <input type="file" ref="refInput" accept="video/*" style="display: none;" @change="handleFileChange('ref', $event)">
                        </div>
                    </div>
                    <div class="process">
                        Process
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// import { ref } from 'vue';

export default {
    name: 'MediaView',
    data() {
        return {
            selectedOption: 'Squat', // 默认选中的值
            oriVideo: null,
            refVideo: null,
            currentVideo: null, // 当前展示的视频
            oriVideoCover: null, // 存储ori视频封面图的 URL
            refVideoCover: null, // 存储ref视频封面图的 URL
        };
    },

    // computed: {
    //     // 动态设置 update-ori 和 update-ref 的背景色
    //     updateOriAndRef(target) {
    //         if (target == 'ori') {
    //             return {
    //                 backgroundColor: this.oriVideo && this.currentVideo && this.currentVideo == this.oriVideo ? '#D9D9D9' : '#FFFFFF',
    //             };
    //         }
    //         else if (target == 'ref') {
    //             return {
    //                 backgroundColor: this.refVideo && this.currentVideo && this.currentVideo == this.refVideo ? '#D9D9D9' : '#FFFFFF',
    //             };
    //         }
            
    //     }
    // },
    // computed 返回的是计算值

    methods: {
        // 触发文件选择
        triggerFileInput(target) {
            this.$refs[`${target}Input`].click();
        },

        handleUploadClick(target) {
            let video = null;
            if (target === 'ori') {
                video = this.oriVideo;
            } else if (target === 'ref') {
                video = this.refVideo;
            }
            if (video) {
                this.currentVideo = video;
            } else {
                this.triggerFileInput(target);
            }
            
        },

        // 处理文件选择
        handleFileChange(target, event) {
            const file = event.target.files[0]; // 获取选择的文件
            if (!file) {
                return;
            }
            console.log(file);
            // 生成文件URL
            const url = URL.createObjectURL(file);

            // 更新数据
            this[`${target}Video`] = url;
            this.currentVideo = this[`${target}Video`];

            // 生成视频封面
            this.generateVideoCover(target, file);

            // 清除输入以便重复上传
            event.target.value = null; // ori/ref+Input
        },

        generateVideoCover(target, file) {
            const video = document.createElement('video');
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');

            // 设置视频源
            video.src = URL.createObjectURL(file);

            // 等待视频元数据加载完成
            video.addEventListener('loadedmetadata', () => {
                // 设置canvas尺寸与视频尺寸一致
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;

                // 等待视频播放到第一帧
                video.currentTime = 0;
                video.addEventListener('seeked', () => {
                    // 绘制视频帧到canvas
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);

                    // 生成封面图的URL
                    if (target === 'ori') {
                        this.oriVideoCover = canvas.toDataURL('image/png');
                    } else if (target === 'ref') {
                        this.refVideoCover = canvas.toDataURL('image/png');
                    }

                    // 释放资源URL
                    URL.revokeObjectURL(video.src);
                })
            })
        },

        // 动态设置背景颜色
        getBackgroundColor(target) {
            if (target === 'ori') {
                return {
                    backgroundColor: this.oriVideo && this.currentVideo === this.oriVideo ? '#D9D9D9' : '#FFFFFF',
                };
            } else if (target === 'ref') {
                return {
                    backgroundColor: this.refVideo && this.currentVideo === this.refVideo ? '#D9D9D9' : '#FFFFFF',
                };
            }
            return {}; // 默认返回空对象
        },
    },

    beforeDestroy() {
        // 释放资源URL
        URL.revokeObjectURL(this.oriVideo);
        URL.revokeObjectURL(this.refVideo);
    },


    // setup() {
    //     const oriinput = ref(null);

    //     const triggerFileInput = (target) => {
    //         ['${target}input'].value.click();
    //     }

    //     const handleFileChange = () => {
    //         console.log(oriinput.value.files[0]);
    //     };

    //     return {
    //         oriinput,
    //         triggerFileInput,
    //         handleFileChange,
    //     };
    // },
};
</script>

<style scoped>
.container {
    /* 保持长宽比 345：376 */
    aspect-ratio: 345 / 376;
    /* 自适应宽度 */
    width: 100%;
    /* height: 100%; */
    /* 布局 */
    display: flex;
    /* 交叉轴 */
    align-items: center;
    /* 主轴 */
    flex-direction: column;
    /* justify-content: flex-start; */
    /* 样式 */
    /* padding: 5px; 内边距 */
    /* box-sizing: border-box; */
}

.header {
    /* 保持长宽比 345：39 */
    /* aspect-ratio: 345 / 39; */
    width: 100%;
    height: 10.3%;
    display: flex;
    align-items: center;
    justify-content: space-between;

    background-color: #F3F3F3;

    padding: 0 10px;
    box-sizing: border-box;
}

.title {
    font-size: 20px; /* 标题字体大小 */
    font-weight: bold;
}

.help {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.content-container {
    /* 保持长宽比 345：337 */
    aspect-ratio: 345 / 337;
    width: 100%;
    display: flex;
    padding: 5px;
    justify-content: center;
    align-items: center;

    background-color: #FFFFFF;
    box-sizing: border-box;
}

.content {
    /* 335.22*322 */
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0 5px;
    border-radius: 8px; /* 圆角 */
    border: 1px solid #EAEAEA;

    /* gap: 5px; */
}

.nav {
    /* 335.22*30 */
    width: 100%;
    height: 9%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2px 5px;
    margin-bottom: 3px;
    /* 分隔线 */
    border-bottom: 1px solid #EAEAEA;
}

.upload {
    /* font-size: 0.8em; */
    font-size: 17px;
    font-weight: bold;
}

.select {
    /* font-size: 0.3em; */
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    width: 60%;
}

/* .select lable {
    display: inline-block;
} */

.selection-box {
    /* 126 * 24 */
    width: 50%;
    height: 100%;

    font-size: 12px;
    border-radius: 5px;
    border: 1px solid #D0D5DD;

    /* margin-left: 5%; */
}

.media-container {
    /* 322*213 */
    width: 100%;
    aspect-ratio: 16 / 9;
    /* height: 66%; */
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px; /* 圆角 */
    /* border: 1px solid #EAEAEA; */
    background-color: #D9D9D9;

    padding: 10px;
    box-sizing: border-box;
    margin-top: 5px;
}

/* 可选方案，效果类似 */
/* .video-wrapper {
    width: 100%;
    aspect-ratio: 16 / 9;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #000;
}

.video-wrapper video {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 8px;
} */

.video-wrapper {
    width: 100%;
    position: relative; /* 相对定位，用于子元素的绝对定位 */
    padding-top: 56.25%; /* 16:9 宽高比 (9 / 16 * 100%) */
    overflow: hidden; /* 隐藏超出部分 */
    background-color: #000;

    border-radius: 5px;
}

.video-wrapper video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain; /* 保持视频比例，完整显示视频内容 */
    border-radius: 5px;
}



.operation-container {
    /* 322*65 */
    width: 100%;
    /* height: 20%; */
    height: 23%;
    display: flex;
    align-items: center;
    /* justify-content: space-between; */
}

.update-ori {
    /* 79*65 */
    width: 25%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px; /* 圆角 */
    padding: 5px;
    /* border: 1px solid #EAEAEA; */
    /* background-color: #D9D9D9; */
    box-sizing: border-box;
}

.update-ref {
    /* 79*65 */
    width: 25%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px; /* 圆角 */
    padding: 5px;
    /* border: 1px solid #EAEAEA; */
    /* background-color: #D9D9D9; */
    box-sizing: border-box;
    /* 默认情况下，CSS 使用 标准盒模型（content-box），即元素的宽度和高度仅包括内容区域，不包括内边距和边框。 */
    /* border-box：宽度和高度包括内容区域、内边距和边框。内边距和边框不会增加元素的总尺寸。 */
}

.upload-icon {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    /* padding: 5px; */
    border: 1px dashed #000000;
    /* box-sizing: border-box; */

    position: relative; /* 相对定位，用于子元素的绝对定位 */
}

.video-cover {
    width: 100%;
    height: 100%;;
    object-fit: fill; /* 保持封面图比例，填充整个图标 */
}

.upload-icon-img {
    width: 60%;
    height: 60%;
    object-fit: fill; /* 保持图标比例，填充整个图标 */
    
    /* margin: 5px;
    box-sizing: border-box; */
}

.process {
    width: 50%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px; /* 圆角 */
    /* border: 1px solid #EAEAEA; */
    background-color: #D9D9D9;
    /* 字体 */
    font-size: 1.5em;
    font-weight: bold;
}

.label-box {
    position: absolute;
    top: 0;
    left: 0;
    background-color: white;
    padding: 1px 3px;
    border-radius: 3px;
    font-size: 8px;
    font-weight: bold;
    z-index: 1; /* 确保白色框在视频和图标之上 */
}

</style>