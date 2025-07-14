<template>
    <div class="container">
        <div class="header">
            <div class="title">Assessment View</div>
            <div class="upload-icon">
                <!-- <img src="@/assets/image 49.png" alt="upload" height="100%"> -->
                <img src="@/assets/assess_upload.png" alt="upload" height="100%">
            </div>
        </div>

        <div class="content-container">
            <div class="content">
                <div class="content-nav">
                    <div class="content-title">
                        Sumo Squat
                    </div>
                    <div class="tools">
                        <div class="refresh-icon">
                            <!-- <img src="@/assets/image 587.png" alt="refresh" height="100%"> -->
                            <img src="@/assets/assess_refresh.png" alt="refresh" height="100%">
                        </div>
                        <div class="save-icon">
                            <!-- <img src="@/assets/image 52.png" alt="save" height="100%"> -->
                            <img src="@/assets/assess_save.png" alt="save" height="100%">
                        </div>
                    </div>
                </div>

                <div class="separator"></div>
                <!-- <hr class="separator"></hr> -->

                <!-- Segment content to display the image -->
                <div class="segment-content">
                    <!-- <img :src="currentImage" alt="segment image" class="segment-image" /> -->
                    <ImageWithKeypoints 
                        :image-src="currentImage"
                        :constraints="currentConstraints"
                        :keypoints="currentKeypoints"
                    />
                </div>

                <div class="separator"></div>

                <div class="segment-options">
                    <!-- Dynamically generate segment-select based on assessment count -->
                    <div 
                        class="segment-select"
                        v-for="(assessment, index) in assessments"
                        :key="assessment.id"
                        @click="selectSegment(index)"
                        :class="{ active: selectedSegment === index }"
                    >
                        <!-- 1 -->
                        {{ index + 1 }}
                    </div>

                    <div class="confirm-icon">
                        <!-- <img src="@/assets/image 577.png" alt="confirm" height="100%"> -->
                        <img src="@/assets/assess_done.png" alt="confirm" height="80%">
                    </div>
                </div>
            </div>

            <div class="template">
                <div class="template-nav">
                    <div class="template-title">
                        Template
                    </div>
                    <div class="search">
                        <div class="search-text">
                            Search text
                        </div>
                        <div class="search-icon">
                            <img src="@/assets/assess_search.png" alt="search" height="100%">
                        </div>
                        <div class="sort-icon">
                            <img src="@/assets/assess_icon.png" alt="sort" height="100%">
                        </div>
                    </div>
                </div>

                <div class="template-list">
                    <div v-for="(template, index) in templates" :key='"template" + index' class="template-item">
                        {{ template }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// import oriData from '@/assets/ori.json';
import refData from '@/assets/ref.json';
import ImageWithKeypoints from '@/components/ImageWithKeypoints.vue';
// import keypointsData1 from '@/assets/sumo_squat_1_keypoints.json'; // 片段1的关键点数据
// import keypointsData2 from '@/assets/sumo_squat_2_keypoints.json'; // 片段2的关键点数据
// import keypointsData3 from '@/assets/sumo_squat_3_keypoints.json'; // 片段3的关键点数据
// import keypointsData4 from '@/assets/sumo_squat_4_keypoints.json'; // 片段4的关键点数据
// import keypointsData1 from '@/assets/sumo_squat_1_keypoints.json'; // 片段1的关键点数据
import keypointsData2 from '@/assets/0062_keypoints.json'; // 片段2的关键点数据
import keypointsData3 from '@/assets/0091_keypoints.json'; // 片段3的关键点数据
import keypointsData4 from '@/assets/0123_keypoints.json'; // 片段4的关键点数据

export default {
    name: 'AssessmentView',
    components: {
        ImageWithKeypoints, // Register the new component
    },
    data() {
        return {
            assessments: [],
            selectedSegment: 0, // Default to segment 1 (index 0)
            segmentImages: [
                // require('@/assets/sumo_squat_1.png'), // Image for segment 1
                // require('@/assets/sumo_squat_2.png'), // Image for segment 2
                // require('@/assets/sumo_squat_3.png'), // Image for segment 3
                // require('@/assets/sumo_squat_4.png'), // Image for segment 4
                // require('@/assets/sumo_squat_1.png'), // Image for segment 1
                require('@/assets/0062.png'), // Image for segment 2
                require('@/assets/0091.png'), // Image for segment 3
                require('@/assets/0123.png'), // Image for segment 4
            ],
            keypointsData: [
                // keypointsData1, // 片段1的关键点数据
                keypointsData2, // 片段2的关键点数据
                keypointsData3, // 片段3的关键点数据
                keypointsData4, // 片段4的关键点数据
            ],
            templates: [
                'Sumo Squat',
                'Sumo Squat',
                'Sumo Squat',
                'Sumo Squat',
                'Sumo Squat',
            ],
        }
    },
    computed: {
        currentImage() {
            // Return the image for the currently selected segment
            return this.segmentImages[this.selectedSegment];
        },
        currentConstraints() {
            // 获取当前选中的 segment 的 constraints
            console.log(this.assessments[this.selectedSegment]?.constraints || [])
            return this.assessments[this.selectedSegment]?.constraints || [];
        },
        currentKeypoints() {
            return this.keypointsData[this.selectedSegment]; // 返回当前片段的关键点数据
        },
    },
    created() {
        this.loadAssessmentData();
    },
    methods: {
        loadAssessmentData() {
            // this.assessments = oriData.assessment;
            this.assessments = refData.assessment;

            // 过滤掉 constraints 为空的 assessment
            this.assessments = this.assessments.filter(assessment => {
                return assessment.constraints && assessment.constraints.length > 0;
            });

            console.log('Assessments:', this.assessments);
        },
        selectSegment(index) {
            this.selectedSegment = index;
            console.log('Selected segment:', index + 1);
        }
    },

}
</script>

<style scoped>
.container {
    /* 保持长宽比 345：629 */
    aspect-ratio: 345 / 629;
    /* 自适应宽度 */
    width: 100%;
    /* height: 100%; */
    height: 59.1%;
    /* 布局 */
    display: flex;
    /* flex: 1; */
    flex-direction: column;
    align-items: center;
    /* padding: 5px; 内边距 */
    /* box-sizing: border-box; */
    /* align-items: stretch; */
    /* overflow: hidden; */
    /* height: 0; */
}

.header {
    /* 保持长宽比 345：39 */
    /* aspect-ratio: 345 / 39; */
    /* 冲突？ */
    width: 100%;
    height: 6%;
    display: flex;
    align-items: center;
    justify-content: space-between;

    background-color: #F3F3F3;

    padding: 0 10px;
    box-sizing: border-box;
}

.title {
    font-size: 20px;
    font-weight: bold;
}

.upload-icon {
    height: 100%;
    /* width: 100%; */
    display: flex;
    align-items: center;
    justify-content: center;

}

.content-container {
    /* 保持长宽比 345：590 */
    aspect-ratio: 345 / 590;
    width: 100%;
    height: 579.94px;
    display: flex;
    padding: 5px;
    flex-direction: column;
    align-items: center;
    box-sizing: border-box;

    background-color: #FFFFFF;
    gap: 10px;
}

.content {
    /* 335.22*435 */
    width: 100%;
    /* height: 73.7%; */
    height: 78%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 5px;
    border-radius: 8px; /* 圆角 */
    border: 1px solid #EAEAEA; /* 边框 */

    box-sizing: border-box;
    overflow: hidden; /* 防止内容溢出 */
}

.content-nav {
    /* 335.22*34 */
    width: 100%;
    /* height: 7.8%; */
    height: 7%;
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 5px;
    box-sizing: border-box;
}

.content-title {
    /* font-size: 0.8em; */
    font-size: 17px;
    font-weight: bold;
}

.tools {
    height: 100%;
    display: flex;
    align-items: center;
}

.refresh-icon {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.save-icon {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.separator {
    width: 100%; /* 分隔线宽度 */
    height: 1px; /* 分隔线高度 */
    background-color: #EAEAEA; /* 分隔线颜色 */
    margin: 3px 0; /* 分隔线与元素的间距 */
}

.segment-content {
    /* 331*326 */
    width: 100%;
    /* height: 74.9%; */
    height: 76%;
    display: flex;
    flex-direction: column;
    /* align-items: center; */
    /* justify-content: center; */
    /* box-sizing: border-box; */
    /* min-height: 0; */
    overflow: hidden; /* 防止内容溢出 */

    /* padding: 5px 0; */
    /* box-sizing: border-box; */
}

/* .segment-image {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
} */

.segment-options {
    width: 100%;
    height: 12%;
    display: flex;
    align-items: center;
    /* justify-content: space-between; */
    justify-content: flex-start;
    
    padding: 0 5px;
    box-sizing: border-box;

    gap: 10px;
}

.segment-select {
    /* 50*50 */
    width: 14.9%;
    aspect-ratio: 1 / 1;
    /* height: 11.5%; */
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #D9D9D9;

    font-weight: bold;
}

.segment-select.active {
    background-color: #A9A9A9; /* Highlight the selected segment */
}

.confirm-icon {
    height: 100%;
    display: flex;
    align-items: center;

    margin-left: auto; /* 靠右放置 */
}

.template {
    /* 335.22*126 */
    width: 100%;
    /* height: 21.4%; */
    height: 18%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 5px;
    border-radius: 8px; /* 圆角 */
    border: 1px solid #EAEAEA; /* 边框 */

    box-sizing: border-box;
}

.template-nav {
    /* 335.22*34 */
    width: 100%;
    height: 33%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 5px;
    border-bottom: 1px solid #EAEAEA;
    box-sizing: border-box;
}

.template-title {
    /* font-size: 0.8em; */
    font-size: 17px;
    font-weight: bold;
}

.search {
    height: 100%;
    display: flex;
    align-items: center;
}

.search-text {
    white-space: nowrap;
    font-size: 12px;
    margin-right: 5px;
}

.search-icon {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.sort-icon {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.template-list {
    /* 335.22*92 */
    width: 100%;
    height: 73%;
    display: flex;
    padding: 5px;
    align-items: flex-start;
    box-sizing: border-box;

    gap: 2px 10px;
    padding-bottom: 0px;
    flex-wrap: wrap;
    overflow-y: auto;
}

.template-item {
    /* 65*25 */
    /* width: 19.4%; */
    width: 22%;
    aspect-ratio: 65 / 25;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #D9D9D9;

    font-size: 10px;
    /* font-size: 0.1em; */
}
</style>