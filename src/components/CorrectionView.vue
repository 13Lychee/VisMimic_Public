<template>
    <div class="container">
        <div class="header">
            <div class="title">
                Correction View
            </div>
            <div class="edit-icon">
                <img src="@/assets/image 625.png" alt="edit" height="100%">
            </div>
        </div>
        <div class="content-container">
            <svg class="correction-view-svg" width="100%" height="100%">
                <!-- 水平线 1509*17 靠右 距上130 #D9D9D9 -->
                <line
                    x1="3%"
                    y1="57%"
                    x2="100%"
                    y2="57%"
                    stroke="#D9D9D9"
                    stroke-width="12"
                />

                <!-- 竖直线和端点 -->
                <!-- <line
                    v-if="selectedNumber !== null"
                    :x1="`${3 + (selectedNumber * 24.25)}%`"
                    y1="10%"
                    :x2="`${3 + (selectedNumber * 24.25)}%`"
                    y2="90%"
                    stroke="#C59CF4"
                    stroke-width="2"
                /> -->
                <line
                    v-if="selectedNumber !== null"
                    :x1="getXPosition(selectedNumber)"
                    y1="10%"
                    :x2="getXPosition(selectedNumber)"
                    y2="90%"
                    stroke="#C59CF4"
                    stroke-width="2"
                />
                <circle
                    v-if="selectedNumber !== null"
                    :cx="getXPosition(selectedNumber)"
                    cy="10%"
                    r="7"
                    fill="#C59CF4"
                />
                <circle
                    v-if="selectedNumber !== null"
                    :cx="getXPosition(selectedNumber)"
                    cy="90%"
                    r="7"
                    fill="#C59CF4"
                />
            </svg>

            <!-- 绘制序号圆点 -->
            <div
                v-for="n in 4"
                :key="'number' + n - 1"
                class="number-circle"
                :style="{
                    left: getXPosition(n - 1),
                    top: '57%',
                    borderColor: selectedNumber === n - 1 ? '#C59CF4' : '#A3A3A3',
                }"
                @click="selectNumber(n - 1)"
            >
                {{ n - 1 }}
            </div>

            <!-- 上方建议列表 -->
            <div 
                v-for="(advice, index) in adviceList"
                :key="'advice-' + index"
                class="advice-list"
                :style="{
                    left: getXPosition(index, 5),
                    top: '8%',
                }"
            >
                <div
                    v-for="(item, i) in advice"
                    :key="'advice-' + index +'-item-' + i"
                    class="advice-item"
                >
                    <input 
                        type="checkbox" 
                        :id="'advice-' + index +'-item-' + i" 
                        v-model="item.checked"
                    ></input>
                    <!-- <label for="'advice-' + index +'-item-' + i">{{ item.text }}</label> -->
                    <label 
                        :for="'advice-' + index +'-item-' + i" 
                        v-html="highlightKeywords(item.text)"
                        :title="item.text"
                        :class="{ 'selected-advice': isAdviceSelected(index, i, $event) }"
                        @click="selectAdvice(index, i)"
                    >
                    </label>
                </div>
                <div v-if="advice.length !== 0" class="advice-item">
                    <!-- <font-awesome-icon :icon="['far', 'square-plus']" class="add-icon" size="lg" /> -->
                    <!-- <i class="fa-regular fa-square-plus add-icon"></i> -->
                    <div class="correction-add-icon">
                        <img src="@/assets/correction_add.png" alt="add" height="100%">
                    </div>
                    <div class="underline-after"></div>
                </div>
            </div>

            <!-- 下方指导 -->
            <div
                v-for="(instruction, index) in instructionList"
                :key="'instruction-' + index"
                class="instruction-item"
                :style="{
                    left: getXPosition(index, 5.5),
                    top: '65%',
                }"
            >
                {{ instruction.length ? '"' : '' }}{{ instruction }}{{ instruction.length ? '"' : '' }}
            </div>
        </div>
    </div>
</template>

<script>
import sumoCorrectData from '@/assets/sumo_correct.json'; // 导入 sumo_correct.json 文件
import { EventBus } from '@/eventBus'; // 导入 Event Bus

export default {
    name: 'CorrectionView',
    data() {
        return {
            selectedNumber: 1,
            adviceList: [
                [

                ],
                [
                    { text: "Keep raise your head up.", checked: true },
                    { text: "Keep your back straight.", checked: false },
                    { text: "Stand with your feet wide apart.", checked: false },
                ],
                [
                    { text: "Keep raise your head up.", checked: true },
                    { text: "Keep your back straight.", checked: false },
                    { text: "Stand with your feet wide apart.", checked: false },
                ],
                [
                    { text: "Keep raise your head up.", checked: true },
                    { text: "Keep your back straight.", checked: false },
                    { text: "Stand with your feet wide apart.", checked: false },
                ],
            ],
            instructionList: [
                "",
                "“stand about twice shoulder-width apart, with your toes facing diagonally forward.”",
                "“when squatting to the thighs parallel to the ground, keep your knees in the same direction as your toes.”",
                "“keep your upper body as straight as possible. cross your arms over your chest.”",
            ],
            selectedAdvice: null, // 记录选中的advice {listIndex, itemIndex}
        };
    },
    created() {
        this.loadCorrectionData(); // 在组件创建时加载数据

        // 从 localStorage 中读取 selectedNumber
        // const savedSelectedNumber = localStorage.getItem('selectedNumber');
        // if (savedSelectedNumber !== null) {
        //     this.selectedNumber = Number(savedSelectedNumber); // 如果存在，使用存储的值
        // } else {
        //     // 如果不存在，存储默认值到 localStorage
        //     localStorage.setItem('selectedNumber', this.selectedNumber.toString());
        // }
        // localStorage.setItem('selectedNumber', this.selectedNumber.toString());

        const number = this.selectedNumber;
        EventBus.emit('correction-selected-number-changed', number); // 发布事件
        EventBus.emit('correction-selected-advice-changed', this.selectedAdvice); // 发布事件
    },
    methods: {
        /**
         * 处理单选框点击事件
         */
        //  handleCheckboxClick(listIndex, itemIndex, event) {
        //     // 阻止默认行为（因为 v-model 会处理勾选状态）
        //     // event.preventDefault();
        //     // 手动切换勾选状态
        //     this.adviceList[listIndex][itemIndex].checked = !this.adviceList[listIndex][itemIndex].checked;
        // },

        /**
         * 选中指定的advice
         */
        selectAdvice(listIndex, itemIndex, event) {
            // 阻止默认行为（因为 v-model 会处理勾选状态）
            // event.preventDefault();
            // event.stopPropagation();
            // this.selectedAdvice = { listIndex, itemIndex };
            if (this.isAdviceSelected(listIndex, itemIndex)) {
                // 如果已经选中，则取消选中
                this.selectedAdvice = null;
            } else {
                // 否则选中该建议
                this.selectedAdvice = { listIndex, itemIndex };
            }
            EventBus.emit('correction-selected-advice-changed', this.selectedAdvice); // 发布事件
        },

        /**
         * 判断当前advice是否被选中
         */
         isAdviceSelected(listIndex, itemIndex) {
            return this.selectedAdvice && 
                   this.selectedAdvice.listIndex === listIndex && 
                   this.selectedAdvice.itemIndex === itemIndex;
        },

        /**
         * 高亮文本中的特定单词
         * @param {string} text - 原始文本
         * @returns {string} - 高亮后的 HTML 文本
         */
        highlightKeywords(text) {
            const keywords = ['head', 'back', 'feet', 'toes', 'knees', 'thighs', 'spine', 'hips'];
            // 这种写法也对
            // const regex = new RegExp(`\\b(${keywords.join('|')})\\b`, 'gi');
            // return text.replace(regex, '<span style="color: #F7877C;">$1</span>');

            // 遍历需要高亮的单词
            keywords.forEach((word) => {
                const regex = new RegExp(`\\b${word}\\b`, 'gi'); // 匹配单词（不区分大小写）
                text = text.replace(
                regex,
                `<span style="color: #F7877C;">${word}</span>`
                );
            });
            return text;
        },
        /**
         * 选择序号
         * @param {number} number - 选中的序号
         */
        selectNumber(number) {
            this.selectedNumber = number;

            // 将 selectedNumber 存储到 localStorage
            // localStorage.setItem('selectedNumber', number.toString());

            EventBus.emit('correction-selected-number-changed', number); // 发布事件

            console.log('Selected segment:', number + 1);
        },
        /**
         * 加载校正数据
         */
         loadCorrectionData() {
            // 从 sumo_correct.json 中读取数据
            // this.instructionList = sumoCorrectData.correction.map(item => item.dataset);
            this.instructionList = [];
            this.instructionList = sumoCorrectData.correction.map(item => 
                item.feedbacks.length > 0 ? item.dataset : '' // 如果 feedbacks 为空，dataset 置为空
            );

            // this.adviceList = [];
            // this.adviceList = sumoCorrectData.correction.map(item => 
            //     item.feedbacks.map(feedback => ({
            //         text: feedback.text,
            //         checked: false, // 默认未选中
            //     }))
            // );
            this.adviceList = sumoCorrectData.correction.map(item => 
                item.feedbacks.length > 0 
                    ? item.feedbacks.map(feedback => ({
                        text: feedback.text,
                        checked: false, // 默认未选中
                    }))
                    : [] // 如果 feedbacks 为空，adviceList 对应项为空数组
            );

            console.log('Instruction List:', this.instructionList);
            console.log('Advice List:', this.adviceList);
        },

        /**
         * 计算横轴 x 坐标
         * @param {number} index - 当前序号
         * @param {number} offset - 起始偏移量，默认为 3
         * @returns {string} - 计算后的 x 坐标（百分比）
         */
         getXPosition(index, offset = 3) {
            // return `${offset + (index * 24.25)}%`;
            if (index === 0) {
                return `${offset}%`;
            }
            return `${offset + (index * 26) - 7}%`;
        },
    },
};
</script>

<style scoped>
.container {
    /* 长宽改为1553*266 */
    /* 保持长宽比 1160：254 -> 1553: 266 */
    /* aspect-ratio: 1160 / 254; */
    aspect-ratio: 1553 / 266;
    /* 自适应宽度 */
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    /* padding: 5px; 内边距 */
    /* box-sizing: border-box; */
}

.header {
    /* 保持长宽比 1160：39 -> 1553: 39 */
    /* aspect-ratio: 1160 / 39; */
    /* aspect-ratio: 1553 / 39; */
    width: 100%;
    /* height: 15.4%; */
    height: 14.6%;
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

.edit-icon {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.content-container {
    /* 保持长宽比 1160：214 -> 1553: 227 */
    /* aspect-ratio: 1160 / 214; */
    aspect-ratio: 1553 / 227;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    /* padding: 5px; */
    /* box-sizing: border-box; */

    background-color: #FFFFFF;

    position: relative;

    /* overflow-x: auto; */
    overflow-x: scroll;
}

.correction-view-svg {
    position: absolute;
    top: 0;
    left: 0;
}

.number-circle {
    /* 50 * 50 */
    /* 宽高均为 35px */
    position: absolute;
    width: 21px;
    height: 21px;
    border-radius: 50%;
    background-color: #FFFFFF;
    border: 7px solid #A3A3A3;
    transform: translate(-50%, -50%);

    /* z-index: 1; */
    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 0.8em;
    font-weight: bold;
    color: #000000;
}

.advice-list {
    position: absolute;
    width: 23%;
    height: 50%;

    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
}

.advice-item {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;

    font-size: 16px;
    color: #2E4051;
    text-align: left;

    overflow: hidden;
}

.selected-advice {
    background-color: #F0E6FF;
    border-radius: 4px;
}

.advice-item label {
    /* 新增样式，使advice-item中的建议文本只显示一行，超出则显示... */
    white-space: nowrap; /* 禁止换行 */
    overflow: hidden; /* 超出部分隐藏 */
    text-overflow: ellipsis; /* 超出部分显示省略号 */
    /* word-break: keep-all; */
    /* overflow-wrap: break-word; */
    /* display: -webkit-box; */
    /* -webkit-box-orient: vertical; */
    /* -webkit-line-clamp: 1; */
    
    /* display: inline-block; */
    /* min-width: 0; */
    /* max-width: 90%; */
}

.correction-add-icon {
    /* width: 100%; */
    height: 19.5px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: 1px;
}

.add-icon {
    margin: 1px 3px 3px 4px;
    /* height: 13px; */
}

.underline-after {
    width: 100%;
    height: 100%;
    position: relative;
}

.underline-after::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: 25%;
    width: 50%;
    height: 1px;
    background-color: black;
}

.instruction-item {
    position: absolute;
    width: 22%;
    height: 30%;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;

    font-size: 16px;
    color: #2E4051;
    font-style: italic;
    text-align: left;
}
</style>