<template>
    <div class="container">
        <div class="header">
            <div 
                class="ExplorationView-title"
                :class="{ active: selectedView === 'exploration' }"
                @click="setSelectedView('exploration')"
            >
                <!-- <img class="ExplorationView-title-icon" src="@/assets/image 623.png" alt="exploration view"> -->
                <img class="ExplorationView-title-icon" src="@/assets/explorationview.png" alt="exploration view">
                Exploration View
            </div>
            <div class="EditionView-title"
                :class="{ active: selectedView === 'edition' }"
                @click="setSelectedView('edition')"
            >
                <!-- <img class="EditionView-title-icon" src="@/assets/Frame.png" alt="edition view"> -->
                <img class="EditionView-title-icon" src="@/assets/editionview.png" alt="edition view">
                Edition View
            </div>
        </div>

        <div v-if="selectedView === 'exploration'" class="content-container">
            <div class="media-container" style="overflow-x: hidden;">
                <div v-show="ExplorationView_mode === 'compare'" class="playMenu-container">
                    <div class="playMenu">
                        <img class="playMenu-icon" src="/L5.png">
                        <img class="playMenu-icon" src="/L.png">
                        <img class="playMenu-icon" src="/Mplay.png">
                        <img class="playMenu-icon" src="/R.png">
                        <img class="playMenu-icon" src="/R5.png">
                    </div>
                    <div class="Visualization-option-playMenu">
                        <div class="Visualization-option-title">
                            Speed
                        </div>
                        <div class="Visualization-option-bar">
                            <div  class="Visualization-option-bar-item" >
                                0.5x
                            </div>
                            <div class="Visualization-option-bar-item" >
                                0.75x
                            </div>
                            <div class="Visualization-option-bar-item" >
                                1.0x
                            </div>
                            <div class="Visualization-option-bar-item" >
                                1.5x
                            </div>
                        </div>
                    </div>
                </div>
                
            </div>
            <div class="control-container">
                <!-- 导航栏 -->
                <div class="control-nav">
                    <div 
                        class="display-button"
                        :class="{ active: ExplorationView_mode === 'display' }"
                        @click="ExplorationView_mode = 'display'"
                    >
                        Display
                    </div>
                    <div class="compare-button"
                        :class="{ active: ExplorationView_mode === 'compare' }"
                        @click="ExplorationView_mode = 'compare'"
                    >
                        Compare
                    </div>
                </div>
                <!-- 内容 -->
                <div class="control-content">
                    <div v-if="ExplorationView_mode === 'display'" class="display-mode">
                        <div class="display-selection-area">
                            <select v-model="displayOptions" class="display-selectionBox">
                                <option value="Original Video">Original Video</option>
                                <option value="Original Video">Original Video</option>
                            </select>
                            <div class="display-checkbox">
                                <input type="checkbox" id="withBackgroundVideo" value=true v-model="withBackgroundVideo" checked />
                                <label for="withBackgroundVideo">with background video</label>
                            </div>
                        </div>
                        <div class="horizontal-divider"></div>

                        <div class="display-motion-name-area">
                            <i class="fa-regular fa-lightbulb" style="color: #ffcb3d;"></i>
                            <span class="display-motion-title">Motion: </span>
                            <span class="display-motion-name">Sumo Squat</span>
                            <!-- <div class="display-motion-title">Motion: </div> -->
                            <!-- <div class="display-motion-name">Sumo Squat</div> -->
                        </div>
                        <div class="display-keyattributes-area">
                            <div class="display-keyattributes-title-area">
                                <i class="fa-regular fa-lightbulb" style="color: #ffcb3d;"></i>
                                <span class="display-keyattributes-title">Key Attributes</span>
                            </div>

                            <!-- 遍历 display 数组，生成标题 -->
                            <div v-for="(item, index) in displayData" :key="item.id" class="display-keyattribute-item-area">
                                <div class="display-keyattribute-item-title">
                                    <div class="display-keyattribute-id">
                                        {{ index + 1 }}
                                    </div>
                                    <span class="display-keyattribute-text">{{ item.text }}</span>
                                </div>
                                <!-- 添加折线图容器 -->
                                <div class="chart-container">
                                    <canvas :ref="'display-chart-' + item.id"></canvas>
                                </div>
                            </div>
                        </div>
                        <div class="horizontal-divider"></div>

                        <div class="display-markFrame-area">
                            <div class="display-markFrame-selectionBox-area">
                                <!-- 遍历 display_markedFrames 数组，生成选择框 -->
                                <div 
                                    v-for="(item, index) in display_markedFrames" 
                                    :key="'markFrames-' + index" 
                                    class="display-markFrame-selectionBox"
                                    :style="{ 
                                        borderColor: index === display_currentMarkedBoxId ? '#C59CF4' : item.marked ? '#000000' : '#A3A3A3' 
                                    }"
                                    @click="handleCurrentMarkedBoxIdChange(index)"
                                >
                                    {{ index }}
                                </div>
                                <div class="display-markFrame-selectionBox" @click="handleAddMarkedBox">
                                    +
                                </div>
                            </div>
                            <div class="display-markFrame-button" @click="handleMarkCurrentFrame(display_currentMarkedBoxId, display_currentFrame)">
                                <!-- <i class="fa-regular fa-file-lines"></i> -->
                                <div class="mark-icon">
                                    <img src="@/assets/display_mark.png" alt="mark" height="100%">
                                </div>
                                <span class="display-markFrame-button-text">Mark Current Frame: {{ display_markedFrames[display_currentMarkedBoxId].marked ? display_markedFrames[display_currentMarkedBoxId].frame : display_currentFrame }}</span>
                            </div>
                        </div>
                    </div>
                    <div v-else-if="ExplorationView_mode === 'compare'" class="compare-mode">
                        <div class="compare-selection-area">
                            <select v-model="compareLeftOptions" class="compare-selectionBox">
                                <option value="Original Video">Original Video</option>
                                <option value="Original Video">Original Video</option>
                            </select>
                            vs
                            <select v-model="compareRightOptions" class="compare-selectionBox">
                                <option value="Original Video">Original Video</option>
                                <option value="Original Video">Original Video</option>
                            </select>
                        </div>
                        <div class="compare-comparisonBox-area">
                            <div 
                                v-for="(item, index) in comparisonData" 
                                :key="index" class="compare-comparisonBox"
                                :class="{ 'highlight-box': isComparisonHighlighted(item) }"
                            >
                                <div class="compare-comparisonBox-title">
                                    {{ item.title }}
                                </div>
                                <div class="compare-comparisonBox-content">
                                    <div 
                                        class="compare-comparisonBox-data"
                                        :style="getComparisonColor(item.leftData, item.rightData)"
                                    >
                                        {{ item.leftData }}
                                    </div>
                                    <div class="vertical-divider"></div>
                                    <div 
                                        class="compare-comparisonBox-data"
                                        :style="getComparisonColor(item.leftData, item.rightData)"
                                    >
                                        {{ item.rightData }}
                                    </div>
                                </div>
                            </div>
                            <!-- <div v-for="n in 8" class="compare-comparisonBox">
                                <div class="compare-comparisonBox-title">
                                    Shoulder
                                </div>
                                <div class="compare-comparisonBox-content">
                                    <div class="compare-comparisonBox-data">
                                        35.1°
                                    </div>
                                    <div class="vertical-divider"></div>
                                    <div class="compare-comparisonBox-data">
                                        35.1°
                                    </div>
                                </div>
                            </div> -->
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-else-if="selectedView === 'edition'" class="content-container">
            <div class="media-container" style="overflow-y: scroll;">
                <!-- 四层图片容器 -->

                <div class="background-container"
                    v-for="(item, id) in ref_segs"
                    :key="id"
                    :style="{ transform: `translate(${ id ? ori_segs[id].frame / screenFrames * 100 - 60 : -40 }%, ${ id ? -7 : -35 }%)` }"
                >
                    <img class="stacked-background"
                        :src="currentRefImage(id)"
                    >
                    <div class="background-mark"
                        v-for="(feedback, i) in correction[id].feedbacks"
                        :key="i"
                        :style="getMarkStyle(feedback, id)"
                    >
                        <div class="background-mark-number">
                            {{ feedback.body_part.length }}
                        </div>
                    </div>
                </div>

                <!-- 关键帧控制-->
                <div class="ref-frame"
                    v-for="id in (ref_segs.length - 1)"
                    :key="id"
                    :style="{ transform: `translate(${ id ? ori_segs[id].frame / screenFrames * 100 - 60 : -40 }%, -5%)` }"
                >
                    <div class="frame-number" :class="{ active: activeRefIndex === id }"
                        @click="activeRefIndex = id" 
                        :style="{visibility: (activeRefIndex !== id && activeRefIndex !== null && correctFrame !== null) ? 'hidden' : 'visible'}"
                    >
                        {{ id }}
                    </div>

                    <svg v-if="activeRefIndex === id" class="frame-control-svg" width="100%" height="100%">
                        <line x1="45.5%" y1="120px" x2="50%" y2="159.1px" stroke="#C59CF4" stroke-width="2" />
                        <line x1="50%" y1="120px" x2="50%" y2="159.1px" stroke="#C59CF4" stroke-width="2" />
                        <line x1="670px" y1="120px" x2="50%" y2="159.1px" stroke="#C59CF4" stroke-width="2" />
                        <line x1="670px" y1="120px" x2="1030px" y2="120px" stroke="#C59CF4" stroke-width="2" />
                    </svg>

                    <div v-if="activeRefIndex === id" class="frame-control">            
                        <img class="frame-control-rotate" 
                            src="/rotate.png" 
                            @click="currentRefView[id] = !currentRefView[id]"
                        >
                        <img class="frame-control-play"
                            :src="refIsPlaying ? '/cpause.png' : '/cplay.png'"
                            @click="refIsPlaying = !refIsPlaying"
                        >

                        <div class="frame-problem"
                            v-for="(feedback, i) in correction[id].feedbacks"
                            :key="i"
                            :style="{ left: `${ 150 + i * 300 }px` }"
                            @click="correctFrame = correctFrame === i ? null : i; totalCorrectFrames=frameCorrection[id][i];"
                        >
                            <img class="frame-problem-icon" :src="feedback.img">
                            <div class="frame-problem-text">
                                {{ feedback.text }}
                            </div>
                        </div>

                        <div class="correct-frame"
                            v-if="correctFrame !== null"
                        >

                            <menu class="correct-frame-menu">
                                <div class="correct-frame-menu-title">Menu</div>
                                <div class="correct-frame-menu-item" :class="{active: showCorrectFrame}"
                                    @click="showCorrectFrame = !showCorrectFrame; playCorrectFrame = false;"
                                >
                                    <img src="/animation.png">
                                    Animation
                                </div>

                                <div class="correct-frame-menu-item" :class="{active: playCorrectFrame && showCorrectFrame}"
                                    @click="if (showCorrectFrame) playCorrectFrame = !playCorrectFrame;"
                                >
                                    <img src="/animation-play.png">
                                    Play
                                </div>

                            </menu>

                            <div class="correct-frame-feedback" v-html=highlightKeywords(correction[id].feedbacks[correctFrame].text)>
                            </div>

                            <img class="correct-frame-image"
                                :src="`${basePath_correction}${id.toString().padStart(2, '0')}/${correctFrame.toString().padStart(2, '0')}/background.png`"
                            >
                            <img class="correct-frame-image"
                                v-if="showCorrectFrame"
                                :src="`${basePath_correction}${id.toString().padStart(2, '0')}/${correctFrame.toString().padStart(2, '0')}/${currentCorrectFrame.toString().padStart(4, '0')}.png`"
                            >
                        </div>
                    </div>
                </div>

                <svg class="progress-bar-svg" width="100%" height="100%">
                    <!-- 正视图进度条 -->
                    <!-- 以下第一个line x1 y1对应上面线交叉处，x2 y2对应上面线起点处 -->
                    <line 
                        x1="360px"
                        y1="680px" 
                        x2="20px"
                        y2="450px"
                        stroke="#000000" 
                        stroke-width="1" 
                    />
                    <line 
                        x1="360px"
                        y1="690px" 
                        :x2="`${360 - (360 - 20) * (690 - 460) / (680 - 450)}px`"
                        y2="460px"
                        stroke="#000000" 
                        stroke-width="1" 
                    />
                    <line 
                        v-for="frame in Array.from({ length: Math.ceil(ref_segs[1].frame / 25) }, (_, i) => i * 25)" 
                        :key="'calibration' + frame"
                        :x1 = "`${frame / ref_segs[1].frame * (360 - 20) + 20}px`"
                        :y1 = "`${frame / ref_segs[1].frame * (680 - 450) + 450}px`"
                        :x2 = "`${frame / ref_segs[1].frame * (360 - 20) + 20 + 20}px`"
                        :y2 = "`${frame / ref_segs[1].frame * (680 - 450) + 450}px`"
                        stroke="#000000"
                        stroke-width="1"
                    ></line>
                    <line
                        :x1="`${20 - 10 * Math.cos(Math.atan((680 - 450) / (360 - 20))) / 2 * Math.sin((680 - 450) / (360 - 20))}px`"
                        :y1="`${450 + 10 * Math.cos(Math.atan((680 - 450) / (360 - 20))) / 2 * Math.cos((680 - 450) / (360 - 20))}px`"
                        :x2="`${20 - 10 * Math.cos(Math.atan((680 - 450) / (360 - 20))) / 2 * Math.sin((680 - 450) / (360 - 20)) + Math.min(currentIndex / ref_segs[1].frame * (360 - 20), (360 - 20) + 10 * Math.cos(Math.atan((680 - 450) / (360 - 20))) * Math.sin((680 - 450) / (360 - 20)))}px`"
                        :y2="`${450 + 10 * Math.cos(Math.atan((680 - 450) / (360 - 20))) / 2 * Math.cos((680 - 450) / (360 - 20)) + Math.min(currentIndex / ref_segs[1].frame * (680 - 450), (680 - 450) + 10 * Math.sin(Math.atan((680 - 450) / (360 - 20))) * Math.sin((680 - 450) / (360 - 20)))}px`"
                        stroke="#C59CF4"
                        :stroke-width="`${10 * Math.cos(Math.atan((680 - 450) / (360 - 20)))}px`"
                    ></line>
                    <circle
                        v-if="currentIndex <= ref_segs[1].frame"
                        :cx="`${20 - 10 * Math.cos(Math.atan((680 - 450) / (360 - 20))) / 2 * Math.sin((680 - 450) / (360 - 20)) + currentIndex / ref_segs[1].frame * (360 - 20)}px`"
                        :cy="`${450 + 10 * Math.cos(Math.atan((680 - 450) / (360 - 20))) / 2 * Math.cos((680 - 450) / (360 - 20)) + currentIndex / ref_segs[1].frame * (680 - 450)}px`"
                        :r="`${10 * Math.cos(Math.atan((680 - 450) / (360 - 20))) / 2}px`"
                        fill="#725198"
                        stroke="#725198"
                        stroke-width="0px"
                    ></circle>
                    <!-- <line 
                        :x1="`${ref_segs[1].frame / totalFrames * (1030 - 120) + 120}px`"
                        y1="680px" 
                        :x2="`${ref_segs[1].frame / totalFrames * (1030 - 120) + 120 - 300}px`"
                        :y2="`${680 - 300}px`"
                        stroke="#000000" 
                        stroke-width="1" 
                    />
                    <line 
                        :x1="`${ref_segs[1].frame / totalFrames * (1030 - 120) + 120}px`"
                        y1="690px" 
                        :x2="`${ref_segs[1].frame / totalFrames * (1030 - 120) + 120 - 300}px`"
                        :y2="`${690 - 300}px`"
                        stroke="#000000" 
                        stroke-width="1" 
                    />
                    <line 
                        v-for="frame in Array.from({ length: Math.ceil(ref_segs[1].frame / 25) }, (_, i) => i * 25)" 
                        :key="'calibration' + frame"
                        :x1 = "`${ref_segs[1].frame / totalFrames * (1030 - 120) + 120 - 300 + frame / ref_segs[1].frame * 300}px`"
                        :y1 = "`${680 - 300 + frame / ref_segs[1].frame * 300}px`"
                        :x2 = "`${ref_segs[1].frame / totalFrames * (1030 - 120) + 120 - 300 + frame / ref_segs[1].frame * 300 + 20}px`"
                        :y2 = "`${680 - 300 + frame / ref_segs[1].frame * 300}px`"
                        stroke="#000000"
                        stroke-width="1"
                    ></line>
                    <line
                        :x1="`${ref_segs[1].frame / totalFrames * (1030 - 120) + 120 - 300 - 2.5}px`"
                        :y1="`${680 - 300 + 2.5}px`"
                        :x2="`${ref_segs[1].frame / totalFrames * (1030 - 120) + 120 - 300 - 2.5 + Math.min(currentIndex, ref_segs[1].frame) / ref_segs[1].frame * 300}px`"
                        :y2="`${680 - 300 + 2.5 + Math.min(currentIndex, ref_segs[1].frame) / ref_segs[1].frame * 300}px`"
                        stroke="#C59CF4"
                        stroke-width="7.07px"
                    ></line>
                    <circle
                        v-if="currentIndex <= ref_segs[1].frame"
                        :cx="`${ref_segs[1].frame / totalFrames * (1030 - 120) + 120 - 300 - 2.5 + currentIndex / ref_segs[1].frame * 300}px`"
                        :cy="`${680 - 300 + 2.5 + currentIndex / ref_segs[1].frame * 300}px`"
                        r="3.53px"
                        fill="#725198"
                        stroke="#725198"
                        stroke-width="0px"
                    ></circle> -->
                    <!-- 侧视图进度条 -->
                    <line x1="360px" y1="680px" x2="1200px" y2="680px" stroke="#000000" stroke-width="1" />
                    <line x1="360px" y1="690px" x2="1200px" y2="690px" stroke="#000000" stroke-width="1" />
                    <!-- <line x1="455px" y1="680px" x2="1030px" y2="680px" stroke="#000000" stroke-width="1" /> -->
                    <!-- <line x1="455px" y1="690px" x2="1030px" y2="690px" stroke="#000000" stroke-width="1" /> -->
                    <line 
                        v-for="frame in Array.from({ length: Math.ceil(totalFrames / 25  - Math.ceil(ref_segs[1].frame / 25)) }, (_, i) => (i + Math.ceil(ref_segs[1].frame / 25)) * 25)" 
                        :key="'calibration' + frame"
                        :x1 = "`${(frame - ref_segs[1].frame) / (totalFrames - ref_segs[1].frame) * (1200 - 360) + 360}px`"
                        y1 = 680px
                        :x2 = "`${(frame - ref_segs[1].frame) / (totalFrames - ref_segs[1].frame) * (1200 - 360) + 360 - 20}px`"
                        y2 = 660px
                        stroke="#000000"
                        stroke-width="1"
                    ></line>
                    <!-- <line
                        v-if="currentIndex > ref_segs[1].frame"
                        x1="120px" y1="685px"
                        :x2="`${currentIndex / totalFrames * (1030 - 120) + 120}px`"
                        y2="685px"
                        stroke="#C59CF4"
                        stroke-width="10px"
                    ></line> -->
                    <!-- <line
                        v-if="currentIndex > ref_segs[1].frame"
                        :x1="`${ref_segs[1].frame / totalFrames * (1030 - 120) + 120}px`"
                        y1="685px"
                        :x2="`${currentIndex / totalFrames * (1030 - 120) + 120}px`"
                        y2="685px"
                        stroke="#C59CF4"
                        stroke-width="10px"
                    ></line> -->
                    <line
                        v-if="currentIndex > ref_segs[1].frame"
                        x1="360px"
                        y1="685px"
                        :x2="`${(currentIndex - ref_segs[1].frame) / (totalFrames - ref_segs[1].frame) * (1200 - 360) + 360}px`"
                        y2="685px"
                        stroke="#C59CF4"
                        stroke-width="10px"
                    ></line>
                    <circle
                        v-if="currentIndex > ref_segs[1].frame"
                        :cx="`${(currentIndex - ref_segs[1].frame) / (totalFrames - ref_segs[1].frame) * (1200 - 360) + 360}px`"
                        cy="685px"
                        r="5px"
                        fill="#725198"
                        stroke="#725198"
                        stroke-width="0px"
                    ></circle>
                    <!-- <line
                        v-for="(segmentation, index) in ref_segs"
                        :key="'line-segmentation' + index"
                        :x1="`${segmentation.frame / totalFrames * (1030 - 120) + 120}px`"
                        y1="690px"
                        :x2="`${segmentation.frame / totalFrames * (1030 - 120) + 120}px`"
                        y2="710px"
                        stroke="#A3A3A3"
                        stroke-width="1px"
                    ></line>
                    <circle
                        v-for="(segmentation, index) in ref_segs"
                        :key="'circle-segmentation' + index"
                        :cx="`${segmentation.frame / totalFrames * (1030 - 120) + 120}px`"
                        cy="710px"
                        r="5px"
                        fill="#FFFFFF"
                        stroke="#A3A3A3"
                        stroke-width="2px"
                    >
                        {{ index }}
                    </circle> -->
                </svg>

                <!-- 动画图片 -->
                
                <!-- 播放按钮 -->
                <img class="animation-button"
                    :src="isPlaying ? '/output-stop.png' : '/output-play.png'"
                    @click="isPlaying = !isPlaying"
                >

                <img class="animation-scale"
                    src="/output-scale.png"
                >

                <div class="animation-container"
                    :style="{ transform: `translate(${ currentIndex / screenFrames * 100 + (currentIndex < ori_segs[1].frame ? -20 * currentIndex / ori_segs[1].frame - 40 : -60) }%, ${currentIndex < ori_segs[1].frame ? -30 + currentIndex / ori_segs[1].frame * 25 : -5}%)` }"
                >
                    <img class="animation-image"
                        :src="currentImage" 
                    >

                    <!-- 动画上面加个标记 -->
                    <div class="animation-mark"
                        :style="getAnimationMarkStyle('hip', currentIndex)"
                    ></div>

                    <div class="animation-mark"
                        v-if="currentIndex < ori_segs[1].frame"
                        :style="getAnimationMarkStyle('left_ankle', currentIndex)"
                    ></div>

                </div>

                <svg width="100%" height="100%" class="animation-svg" v-if="correctFrame === null">
                    <path
                        :d="SmoothPath_y('hip', 0, ori_segs[1].frame + 1)" 
                        fill="none" stroke="#FEBA70" stroke-width="5"
                    />
                    <path 
                        :d="SmoothPath_x('hip', ori_segs[1].frame, totalFrames)" 
                        fill="none" stroke="#FEBA70" stroke-width="5"
                    />
                </svg>
            
            </div>
            <div class="control-container">
                <!-- 导航栏 -->
                <div class="control-nav">
                    <div 
                        class="detail-view-title"
                    >
                        Clip View
                    </div>
                </div>
                <!-- 内容 -->
                <div class="control-content">
                    <div class="detail-view">
                        <div class="Snapshot">
                            <div class="Snapshot-title">
                                Snapshot
                            </div>
                            <div class="clip-horizontal-divider"></div>
                            <div v-if="selectedAdvice" class="Snapshot-content">
                                <div class="Snapshot-content-left">
                                    <div class="Snapshot-key-pose">
                                        <div class="Snapshot-key-pose-title">
                                            Key Pose: 
                                        </div>
                                        <div class="Snapshot-key-pose-no">
                                            {{ selectedAdvice.listIndex}}
                                        </div>
                                    </div>
                                    <div class="Snapshot-frame">
                                        <div class="Snapshot-frame-title">
                                            Frame: 
                                        </div>
                                        <div class="Snapshot-frame-nos">
                                            <div class="Snapshot-frame-start">
                                                {{ selectedAdvice.listIndex > 0 ? correction[selectedAdvice.listIndex - 1].frame : 0 }}
                                            </div>
                                            <div class="Snapshot-frame-end">
                                                {{ correction[selectedAdvice.listIndex].frame }}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="Snapshot-body-part">
                                        <div class="Snapshot-body-part-title">
                                            Body Part: 
                                        </div>
                                        <div class="Snapshot-body-part-items">
                                            <div
                                                v-for="(item, index) in correction[selectedAdvice.listIndex].feedbacks[selectedAdvice.itemIndex].body_part"
                                                :key="'body_part' + index"
                                                class="Snapshot-body-part-item"
                                            >
                                                {{ getBodyPartName(item) }}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="Snapshot-content-right">
                                    <img :src="correction[selectedAdvice.listIndex].feedbacks[selectedAdvice.itemIndex].img" style="width: 100%; object-fit: contain;" alt="snapshot">
                                </div>
                            </div>
                        </div>
                        <div class="Feedback">
                            <div class="Feedback-title">
                                Feedback
                            </div>
                            <div class="clip-horizontal-divider"></div>
                            <div 
                                class="Feedback-content"
                                v-html="FeedbackHighlightKeywords(selectedAdvice ? correction[selectedAdvice.listIndex].feedbacks[selectedAdvice.itemIndex].text : '')"
                            >
                            </div>
                        </div>
                        <div class="Relative-Constraints">
                            <div class="Relative-Constraints-title">
                                Relative-Constraints
                            </div>
                            <div class="clip-horizontal-divider"></div>
                            <div class="Relative-Constraints-content">
                                <div
                                    v-for="(item, index) in correction_selected_relative_constraints"
                                    class="Relative-Constraints-item"
                                    :key="'relative_constraints' + index"
                                >
                                    <div class="Relative-Constraints-item-no">
                                        {{ index + 1 }}
                                    </div>
                                    <div class="Relative-Constraints-item-type">
                                        {{ item.type }}
                                    </div>
                                    <div class="Relative-Constraints-item-joints">
                                        {{ getRelativeConstraintsJoints(item.joints) }}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="Visualization">
                            <div class="Visualization-title">
                                Visualization
                            </div>
                            <div class="clip-horizontal-divider"></div>
                            <div v-if="selectedAdvice" class="Visualization-content">
                                <div class="Visualization-option">
                                    <div class="Visualization-option-title">
                                        Perspective:
                                    </div>
                                    <div class="Visualization-option-bar">
                                        <div 
                                            class="Visualization-option-bar-item" 
                                            :class="{ active: isVisualizationOptionActive(Perspective, 'Front') }"
                                            @click="Perspective = 'Front'"
                                        >
                                            Front
                                        </div>
                                        <div 
                                            class="Visualization-option-bar-item" 
                                            :class="{ active: isVisualizationOptionActive(Perspective, 'Side') }"
                                            @click="Perspective = 'Side'"
                                        >
                                            Side
                                        </div>
                                        <div 
                                            class="Visualization-option-bar-item" 
                                            :class="{ active: isVisualizationOptionActive(Perspective, 'Top') }"
                                            @click="Perspective = 'Top'"
                                        >
                                            Top
                                        </div>
                                    </div>
                                </div>
                                <div class="Visualization-option">
                                    <div class="Visualization-option-title">
                                        Shape:
                                    </div>
                                    <div class="Visualization-option-bar">
                                        <div 
                                            class="Visualization-option-bar-item" 
                                            :class="{ active: isVisualizationOptionActive(Shape, 'Mesh') }"
                                            @click="Shape = 'Mesh'"
                                        >
                                            Mesh
                                        </div>
                                        <div 
                                            class="Visualization-option-bar-item" 
                                            :class="{ active: isVisualizationOptionActive(Shape, 'Skeleton') }"
                                            @click="Shape = 'Skeleton'"
                                        >
                                            Skeleton
                                        </div>
                                    </div>
                                </div>
                                <div class="Visualization-option">
                                    <div class="Visualization-option-title">
                                        Visual Type:
                                    </div>
                                    <div class="Visualization-option-bar">
                                        <div 
                                            class="Visualization-option-bar-item" 
                                            :class="{ active: isVisualizationOptionActive(VisualType, 'Line') }"
                                            @click="VisualType = 'Line'"
                                        >
                                            Line
                                        </div>
                                        <div 
                                            class="Visualization-option-bar-item" 
                                            :class="{ active: isVisualizationOptionActive(VisualType, 'Skeleton') }"
                                            @click="VisualType = 'Skeleton'"
                                        >
                                            Skeleton
                                        </div>
                                    </div>
                                </div>
                                <div class="Visualization-option">
                                    <div class="Visualization-option-title">
                                        Highlight:
                                    </div>
                                    <div class="Visualization-option-bar">
                                        <div 
                                            class="Visualization-option-bar-item" 
                                            :class="{ active: isVisualizationOptionActive(Highlight, 'Marker') }"
                                            @click="Highlight = 'Marker'"
                                        >
                                            Marker
                                        </div>
                                        <div 
                                            class="Visualization-option-bar-item" 
                                            :class="{ active: isVisualizationOptionActive(Highlight, 'Mask') }"
                                            @click="Highlight = 'Mask'"
                                        >
                                            Mask
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- <p>
                            Feedback:
                        </p>
                        <p>
                            Keep raise your <span class="highlight">head</span> up.
                        </p> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import WebGL from 'three/addons/capabilities/WebGL.js';
import { ViewerD, DataParser } from './viewerD.js';
import { ViewerC } from './viewerC.js';
import queryString from 'query-string';
import ref from '../../public/segmentation/ref.json';
import ori from '../../public/segmentation/ori.json';
import cor from '../../public/correction/sumo_correct.json';
import ref_ce from '../../public/ref_line/ceshitu/merge.json';
import ref_zh from '../../public/ref_line/zhengshitu/merge.json';
import ori_ce from '../../public/ori/ceshitu/merge.json';
import ori_zh from '../../public/ori/zhengshitu/merge.json';
import cor_model from '../../public/correction/frames.json';

import assessmentRef from '@/assets/ref.json';
import { EventBus } from '@/eventBus'; // 导入 Event Bus
import displayJsonData from '@/assets/sumo_display.json';
// import correctData from '@/assets/sumo_correct.json';

import { Chart, registerables } from 'chart.js';
import annotationPlugin from 'chartjs-plugin-annotation';
Chart.register(...registerables, annotationPlugin);

export default {
    name: 'ExplorationView',
    data() {
        return {
            selectedView: 'exploration', // exploration, edition
            ExplorationView_mode: 'display', // compare, display
            displayOptions: 'Original Video',
            withBackgroundVideo: true,
            compareLeftOptions: 'Original Video',
            compareRightOptions: 'Original Video',
            app: null,
            fps: 25,
            currentIndex: 1,
            totalFrames: 167, 
            totalFrames_ref: 123,
            screenFrames: 200,
            basePath_ori_ce: '/ori/ceshitu/',
            basePath_ori_zh: '/ori/zhengshitu/',
            basePath_ref_ce: '/ref_line/ceshitu/',
            basePath_ref_zh: '/ref_line/zhengshitu/',
            intervalId: null,
            ref_segs: ref.segmentation,
            ori_segs: ori.segmentation,
            isPlaying: true,
            currentRefIndex: [],
            currentRefView: [],
            refIsPlaying: false,
            activeRefIndex: null,
            refIntervalId: null,
            correction: cor.correction,
            correctFrame: null,
            refKeyPoints_ce: ref_ce,
            refKeyPoints_zh: ref_zh,
            oriKeyPoints_ce: ori_ce,
            oriKeyPoints_zh: ori_zh,
            currentCorrectFrame: 0,
            correctIntervalId: null,
            basePath_correction: '/correction/',
            frameCorrection: cor_model,
            totalCorrectFrames: 0,
            showCorrectFrame: false,
            playCorrectFrame: false,

            correctionSelectedSegment: 1,
            isCompareDataLoaded: false,
            compare_leftPosition: [],
            compare_rightPosition: [],
            compare_currentLeftFrame: 0, // 响应式帧计数器
            compare_currentRightFrame: 0, // 响应式帧计数器
            compare_frameUpdateInterval: null, // 帧更新定时器

            displayData: displayJsonData.display,
            display_frameData: [],
            display_position: [],
            display_chartData: [],
            display_frame: null,
            isDisplayDataLoaded: false,
            display_criticalFrames: [97, 134, 165],
            display_currentFrame: 0, // 响应式帧计数器
            display_frameUpdateInterval: null, // 帧更新定时器
            display_markedFrames: [
                { frame: 62, marked: true},
                { frame: 90, marked: false},
                { frame: 100, marked: false},
                { frame: 110, marked: false},
            ], // 用于存储标记的帧
            display_currentMarkedBoxId: 1, // 当前所选中的标记框的ID
            selectedAdvice: null, // 用于存储当前选中的建议
            correction_selected_relative_constraints: [],
            edition_segmentation_view: [0, 0, 1, 1], // 0 正视图 1 侧视图

            Perspective: 'Front', // Front, Side, Top
            Shape: 'Mesh', // Mesh, Skeleton
            VisualType: 'Line', // Line, Skeleton
            Highlight: 'Marker', // Marker, Mask
        };
    },
    created() {
    //     // 从 localStorage 中读取 selectedNumber
    //     // this.correctionSelectedSegment = localStorage.getItem('selectedNumber');
    //     const savedSelectedSegment = localStorage.getItem('selectedNumber');
    //     this.correctionSelectedSegment = savedSelectedSegment !== null ? Number(savedSelectedSegment) : 2;
    //     console.log(this.correctionSelectedSegment);
        // 订阅事件
        EventBus.on('correction-selected-number-changed', (number) => {
            this.correctionSelectedSegment = number; // 更新 selectedNumber
        });
        EventBus.on('correction-selected-advice-changed', (selectedAdvice) => {
            // console.log(this.correction);
            // console.log("selectedAdvice", selectedAdvice);
            this.selectedAdvice = selectedAdvice;
            if (selectedAdvice === null) {
                this.correction_selected_relative_constraints = [];
                return;
            }
            this.correction_selected_relative_constraints = this.correction[this.selectedAdvice.listIndex].feedbacks[selectedAdvice.itemIndex].relative_constraints;
            console.log("correction_selected_relative_constraints", this.correction_selected_relative_constraints);
        });
    },
    watch: {
        // 监听模式变化
        ExplorationView_mode(newVal) {
            this.destroyViewers();
            this.initViewers();
            console.log('watch', newVal);
            if (newVal === 'compare' && this.selectedView === 'exploration') {
                console.log("ExplorationView_mode: compare");
                this.startCompareFrameListener();
                this.stopDisplayFrameListener();
            }
            
            if (newVal === 'display' && this.selectedView === 'exploration') {
                console.log("ExplorationView_mode: display");
                this.calculateDisplayChartData(this.display_position);
                // console.log("this.display_chartData", this.display_chartData);

                // 更新图表数据
                this.displayData.forEach((item, index) => {
                    // this.initChart(item);
                    const chart = this.$refs['display-chart-' + item.id].chart;
                    console.log("chart", chart);
                    if (chart) {
                        chart.data.labels = this.display_frameData;
                        chart.data.datasets[0].data = this.display_chartData[parseInt(item.id)],
                        console.log("chartData", this.display_chartData[parseInt(item.id)]);
                        chart.update(); // 更新图表
                    }
                });
            }
        },
        selectedView(newVal) {
            this.destroyViewers();
            if (newVal === 'exploration') {
                this.initViewers();
            }
        },
        withBackgroundVideo(newVal) {
            if (this.selectedView === 'exploration' && this.ExplorationView_mode === 'display') {
                if (newVal) {
                    this.app.viewer.showVideo();
                } else {
                    this.app.viewer.hideVideo();
                }
            }
        },
        isPlaying(newVal) {
            if (newVal) {
                this.intervalId = setInterval(() => {
                    this.currentIndex = this.currentIndex % this.totalFrames + 1;
                }, 1000 / this.fps);
            } else if (this.intervalId) {
                clearInterval(this.intervalId);
            }
        },
        refIsPlaying(newVal) {
            if (newVal) {
                if (this.activeRefIndex === this.ref_segs.length - 1) {
                    return;
                }
                this.refIntervalId = setInterval(() => {
                    const len = this.ref_segs[this.activeRefIndex + 1].frame - this.ref_segs[this.activeRefIndex].frame;
                    this.currentRefIndex[this.activeRefIndex] = (this.currentRefIndex[this.activeRefIndex] + 1) % len;
                }, 1000 / this.fps);
            } else if (this.refIntervalId) {
                clearInterval(this.refIntervalId);
            }
        },
        activeRefIndex(oldVal, newVal) {
            if (oldVal !== null && oldVal !== newVal) {
                // this.currentRefIndex[oldVal] = 0;
                this.currentRefIndex.splice(oldVal, 1, 0);
                // this.currentRefView.splice(oldVal, 1, 0);
            }
            if (this.refIntervalId) {
                clearInterval(this.refIntervalId);
            }
            this.refIsPlaying = false;
        },
        correctFrame(newVal) {
            if (this.correctIntervalId) {
                clearInterval(this.correctIntervalId);
            }
            if (newVal !== null) {
                this.currentCorrectFrame = 1;
            }
        },
        playCorrectFrame(newVal) {
            if (newVal) {
                this.correctIntervalId = setInterval(() => {
                    this.currentCorrectFrame = this.currentCorrectFrame % this.totalCorrectFrames + 1;
                }, 1000 / this.fps);
            } else if (this.correctIntervalId) {
                clearInterval(this.correctIntervalId);
            }
        },
        correctionSelectedSegment(newVal) {
            if (newVal === null) {
                return;
            }
            if (this.selectedView === 'exploration') {
                const progress_ref = this.ref_segs[newVal].frame / this.totalFrames_ref;
                const progress_ori = this.ori_segs[newVal].frame / this.totalFrames;
                if (this.ExplorationView_mode === 'display') {
                    this.app.viewer.seekAnimation(progress_ref);
                }else if (this.ExplorationView_mode === 'compare') {
                    this.app.viewer1.seekAnimation(progress_ori);
                    this.app.viewer2.seekAnimation(progress_ref);
                }
            }else if (this.selectedView === 'edition') {
                this.activeRefIndex = newVal;
            }
        },
        display_position: {
            handler(newVal) {
                this.calculateDisplayChartData(newVal);

                // 更新图表数据
                this.displayData.forEach((item, index) => {
                    const chart = this.$refs['display-chart-' + item.id].chart;
                    console.log("chart", chart);
                    if (chart) {
                        chart.data.labels = this.display_frameData;
                        chart.data.datasets[0].data = this.display_chartData[parseInt(item.id)],
                        console.log("chartData", this.display_chartData[parseInt(item.id)]);
                        chart.update(); // 更新图表
                    }
                });
            },
            deep: true // 深度监听，确保数组内部变化也能触发
        },
    },
    mounted() {
        // console.log("frames", this.frameCorrection);
        this.initViewers();
        
        // 背景图片（多张叠加）
        this.currentRefIndex = this.ref_segs.map(() => 0);
        this.currentRefView = this.ref_segs.map(() => 0);
        // 初始使用正面
        this.currentRefView[0] = 1;
        this.currentRefView[1] = 1;

        // 图片序列动画
        this.isPlaying = false;

        // 在组件挂载后初始化图表
        this.displayData.forEach((item) => {
            this.initChart(item);
        });

        this.startDisplayFrameListener();
    },
    beforeUnmount() {
        this.destroyViewers();
        clearInterval(this.intervalId);

        // 取消订阅事件，避免内存泄漏
        EventBus.off('correction-selected-number-changed');
    },
    methods: {
        setSelectedView(view) {
            this.selectedView = view;
        },
        setExplorationViewMode(mode) {
            console.log(mode);
            this.ExplorationView_mode = mode;
        },
        // 初始化查看器
        initViewers() {
            if (this.ExplorationView_mode === 'compare') {
                this.app = new AppC(
                    this.$el.querySelector('.media-container'),
                    window.location,
                    this
                );
            } else if (this.ExplorationView_mode === 'display') {
                this.app = new AppD(
                    this.$el.querySelector('.media-container'),
                    window.location,
                    this
                );
            }
        },
        // 销毁查看器
        destroyViewers() {
            if (this.app) {
                this.app.el.innerHTML = '';  // 清除DOM元素
                this.app = null;
            }
        },
        currentRefImage(id) {
            return (this.currentRefView[id] ? `${this.basePath_ref_zh}` : `${this.basePath_ref_ce}`)
                + `${(this.currentRefIndex[id] + this.ref_segs[id].frame).toString().padStart(4, '0')}.png`;
        },

        highlightKeywords(text) {
            text = "\"" + text + "\"";
            const keywords_bodypart = ['head', 'back', 'feet', 'toes', 'knees', 'thighs', 'spine', 'hips'];
            const keywords_instruction = ['wide', 'outward', 'up', 'straight', 'inward', 'deeper', 'parellel']
            // 这种写法也对
            // const regex = new RegExp(`\\b(${keywords.join('|')})\\b`, 'gi');
            // return text.replace(regex, '<span style="color: #F7877C;">$1</span>');

            // 遍历需要高亮的单词
            keywords_bodypart.forEach((word) => {
                const regex = new RegExp(`\\b${word}\\b`, 'gi'); // 匹配单词（不区分大小写）
                text = text.replace(
                regex,
                `<span style="color: #F7877C;text-decoration: underline;">${word}</span>`
                );
            });

            keywords_instruction.forEach((word) => {
                const regex = new RegExp(`\\b${word}\\b`, 'gi'); // 匹配单词（不区分大小写）
                text = text.replace(
                regex,
                `<span style="color: #FEBA70;text-decoration: underline;">${word}</span>`
                );
            });
            return text;
        },
        // getIndexByJointnameForOriDistance(jointname) {
        //     if (jointname === 'head') {
        //         // Head.position
        //         return 21;
        //     } else if (jointname === 'neck') {
        //         // Neck.position
        //         return 12;
        //     } else if (jointname === 'right_elbow') {
        //         // RightForeArm.position
        //         return 117;
        //     } else if (jointname === 'right_wrist') {
        //         // RightForeArm2.position
        //         return 123;
        //     } else if (jointname === 'left_elbow') {
        //         // LeftForeArm.position
        //         return 39;
        //     } else if (jointname === 'left_wrist') {
        //         // LeftForeArm2.position
        //         return 45;
        //     } else if (jointname === 'hip') {
        //         // Hips.position
        //         return 0;
        //     } else if (jointname === 'right_knee') {
        //         // RightLeg.position
        //         return 207;
        //     } else if (jointname === 'right_ankle') {
        //         // RightFoot.position
        //         return 210;
        //     } else if (jointname === 'left_knee') {
        //         // LeftLeg.position
        //         return 192;
        //     } else if (jointname === 'left_ankle') {
        //         // LeftFoot.position
        //         return 195;
        //     }
        // },
        // getIndexByJointnameForRefDistance(jointname) {
        //     if (jointname === 'head') {
        //         // Head.position
        //         return 21;
        //     } else if (jointname === 'neck') {
        //         // Neck.position
        //         return 12;
        //     } else if (jointname === 'right_elbow') {
        //         // RightForeArm.position
        //         return 147;
        //     } else if (jointname === 'right_wrist') {
        //         // RightForeArm2.position
        //         return 156;
        //     } else if (jointname === 'left_elbow') {
        //         // LeftForeArm.position
        //         return 48;
        //     } else if (jointname === 'left_wrist') {
        //         // LeftForeArm2.position
        //         return 57;
        //     } else if (jointname === 'hip') {
        //         // Hips.position
        //         return 0;
        //     } else if (jointname === 'right_knee') {
        //         // RightLeg.position
        //         return 261;
        //     } else if (jointname === 'right_ankle') {
        //         // RightFoot.position
        //         return 264;
        //     } else if (jointname === 'left_knee') {
        //         // LeftLeg.position
        //         return 243;
        //     } else if (jointname === 'left_ankle') {
        //         // LeftFoot.position
        //         return 246;
        //     }
        // },
        // getIndexByJointnameForAngle() {

        // },
        calculateCompareData(constraint, currentFrame, data) {
            if (data.length === 0) {
                return null;
            }
            console.log("currentFrame", currentFrame);
            
            // 获取constraint中的type
            const type = constraint.type;

            // 根据type获取对应的leftData
            if (type === 'distance') {
                // const point1 = this.app.viewer1.getPosition(this.getIndexByJointnameForDistance(constraint.joints[0].joint_1.name), 0);
                // console.log("data", data);
                // return point1;
                const point1 = constraint.joints[0].joint_1.name;
                const point2 = constraint.joints[1].joint_2.name;
                const property = constraint.joints[0].joint_1.property;
                console.log("point1", point1, "point2", point2, "property", property);

                if (property === 'a' && point1 !== 'ground' && point2 !== 'ground') {
                    const point1_data = data.find(position => position.name === point1);
                    const point2_data = data.find(position => position.name === point2);
                    console.log("point1_data", point1_data, "point2_data", point2_data);
                    if (point1_data && point2_data) {
                        console.log("point1_data", point1_data, "point2_data", point2_data);
                        // point1_data.x是数组数据，还要算出当前帧
                        // const currentFrame = this.app.viewer1.getCurrentFrame();
                        console.log("data", data);
                        console.log("currentFrame", currentFrame);
                        console.log("point1_data.x[currentFrame]", point1_data.x[currentFrame], "point2_data.x[currentFrame]", point2_data.x[currentFrame]);
                        console.log("point1_data.y[currentFrame]", point1_data.y[currentFrame], "point2_data.y[currentFrame]", point2_data.y[currentFrame]);
                        console.log("point1_data.z[currentFrame]", point1_data.z[currentFrame], "point2_data.z[currentFrame]", point2_data.z[currentFrame]);
                        const distance = Math.sqrt(
                            Math.pow(point2_data.x[currentFrame] - point1_data.x[currentFrame], 2) +
                            Math.pow(point2_data.y[currentFrame] - point1_data.y[currentFrame], 2) +
                            Math.pow(point2_data.z[currentFrame] - point1_data.z[currentFrame], 2)
                        );
                        
                        // const distance = 
                        //     Math.pow(point2_data.x[currentFrame] - point1_data.x[currentFrame], 2) +
                        //     Math.pow(point2_data.y[0] - point1_data.y[0], 2) +
                        //     Math.pow(point2_data.z[0] - point1_data.z[0], 2);
                        console.log("distance", distance);
                        return (100 * distance).toFixed(1) + 'cm';
                    }
                } 
                else if (property === 'x' || property === 'y' || property === 'z') {
                    const point1_data = data.find(position => position.name === point1);
                    const point2_data = data.find(position => position.name === point2);
                    if (point1_data && point2_data) {
                        console.log("point1_data", point1_data, "point2_data", point2_data);
                        if (property === 'x') {
                            return (100 * (point2_data.x[currentFrame] - point1_data.x[currentFrame])).toFixed(1) + 'cm';
                        } else if (property === 'y') {
                            return (100 * (point2_data.y[currentFrame] - point1_data.y[currentFrame])).toFixed(1) + 'cm';
                        } else if (property === 'z') {
                            return (100 * (point2_data.z[currentFrame] - point1_data.z[currentFrame])).toFixed(1) + 'cm';
                        }
                    }
                }
                else if (point1 === 'ground' || point2 === 'ground') {
                    const point1_data = data.find(position => position.name === point1);
                    const point2_data = data.find(position => position.name === point2);
                    if (point1_data && point2_data) {
                        console.log("point1_data", point1_data, "point2_data", point2_data);
                        return (100 * Math.abs(point2_data.y[currentFrame] - point1_data.y[currentFrame])).toFixed(1) + 'cm';
                    }
                }
            }

            else if (constraint.type === 'angle') {
                const point1 = constraint.joints[0].joint_1.name;
                const point2 = constraint.joints[1].joint_2.name;
                const point3 = constraint.joints[2].joint_3.name;
                const point1_property = constraint.joints[0].joint_1.property;
                const point2_property = constraint.joints[1].joint_2.property;
                const point3_property = constraint.joints[2].joint_3.property;

                console.log("point1", point1, "point2", point2, "point3", point3);

                // 获取三个节点的坐标
                const point1_data = data.find(position => position.name === point1);
                const point2_data = data.find(position => position.name === point2);
                const point3_data = data.find(position => position.name === point3);

                // if (point1 !== point2 && point2 !== point3) {
                    if (point1_data && point2_data && point3_data) {
                        console.log("point1_data", point1_data, "point2_data", point2_data, "point3_data", point3_data);
                        // point1_data.x是数组数据，还要算出当前帧
                        // 计算向量 BA 和 BC
                        const BA = point1_property === 'a' ? {
                            x: point1_data.x[currentFrame] - point2_data.x[currentFrame],
                            y: point1_data.y[currentFrame] - point2_data.y[currentFrame],
                            z: point1_data.z[currentFrame] - point2_data.z[currentFrame]
                        }: {
                            x: point1_property === 'x' ? 1 : 0,
                            y: point1_property === 'y' ? 1 : 0,
                            z: point1_property === 'z' ? 1 : 0
                        };
                        const BC = point3_property === 'a' ? {
                            x: point3_data.x[currentFrame] - point2_data.x[currentFrame],
                            y: point3_data.y[currentFrame] - point2_data.y[currentFrame],
                            z: point3_data.z[currentFrame] - point2_data.z[currentFrame]
                        } : {
                            x: point3_property === 'x' ? 1 : 0,
                            y: point3_property === 'y' ? 1 : 0,
                            z: point3_property === 'z' ? 1 : 0
                        };

                        // 计算点积
                        const dotProduct = BA.x * BC.x + BA.y * BC.y + BA.z * BC.z;

                        // 计算向量的模长
                        const magnitudeBA = Math.sqrt(BA.x * BA.x + BA.y * BA.y + BA.z * BA.z);
                        const magnitudeBC = Math.sqrt(BC.x * BC.x + BC.y * BC.y + BC.z * BC.z);

                        // 计算夹角的余弦值
                        const cosTheta = dotProduct / (magnitudeBA * magnitudeBC);

                        // 计算夹角（弧度）
                        const thetaRadians = Math.acos(cosTheta);

                        // 将弧度转换为角度
                        const thetaDegrees = thetaRadians * (180 / Math.PI);

                        return thetaDegrees.toFixed(1) + '°';
                    }
                // }
                // else if (point1 === point2) {
                    
                // }
                // else if (point2 === point3) {
                    
                // }
            }
            return '35.1°';
        },

        isComparisonHighlighted(item) {
            if (!this.selectedAdvice || this.selectedAdvice.listIndex !== this.correctionSelectedSegment) {
                return false;
            }

            if (!this.correction_selected_relative_constraints || this.correction_selected_relative_constraints.length === 0) {
                return false;
            }

            // 检查当前比较项的标题是否与选中的约束匹配
            return this.correction_selected_relative_constraints.some(constraint => {
                // 根据约束生成标题，与 comparisonData 中的标题格式一致
                const joints = constraint.joints.map(joint => {
                    const jointName = joint.joint_1?.name || joint.joint_2?.name || joint.joint_3?.name;
                    const property = joint.joint_1?.property || joint.joint_2?.property || joint.joint_3?.property;
                    const simplifiedName = jointName
                        .replace(/left/gi, 'l')
                        .replace(/right/gi, 'r');
                    return property && property !== "a" ? `${simplifiedName}-${property}` : simplifiedName;
                }).filter(Boolean);

                const constraintTitle = `${constraint.type}: ${joints.join(' ~ ')}`;
                return item.title === constraintTitle;
            });
        },

        getComparisonColor(leftData, rightData) {
            // 提取数值部分（假设数据格式为 "35.1°" 或 "35.1cm"）
            const extractValue = (str) => {
                const numStr = str.replace(/[^0-9.-]/g, '');
                return parseFloat(numStr) || 0;
            };

            const leftValue = extractValue(leftData);
            const rightValue = extractValue(rightData);

            // 计算差异百分比（以 rightData 为基准）
            const diffPercentage = Math.abs((leftValue - rightValue) / rightValue) * 100;

            if (diffPercentage <= 10) {
                return { color: '#018D29' }; // 绿色（OK）
            } else if (diffPercentage <= 25) {
                return { color: '#D09837' }; // 黄色（警告）
            } else {
                return { color: '#D75353' }; // 红色（差异大）
            }
        },
        // comparisonData() {
        //     // 获取当前correction view选中的segment
        //     // this.correctionSelectedSegment = localStorage.getItem('selectedNumber');

        //     // 获取当前选中的 assessment
        //     const selectedAssessment = assessmentRef.assessment.find(
        //         assessment => assessment.id === this.correctionSelectedSegment.toString()
        //     );

        //     if (!selectedAssessment || !selectedAssessment.constraints) {
        //         return []; // 如果没有 constraints，返回空数组
        //     }

        //     // 遍历 constraints，生成 title
        //     // return selectedAssessment.constraints.map(constraint => {
        //     //     const joints = Object.values(constraint.joints).map(joint => {
        //     //         return joint.name || joint.joint_1?.name || joint.joint_2?.name || joint.joint_3?.name;
        //     //     }).filter(Boolean); // 过滤掉 undefined

        //     //     return `${constraint.type}: ${joints.join(' ~ ')}`;
        //     // });

        //     // 遍历 constraints，生成包含 title、leftData 和 rightData 的对象
        //     return selectedAssessment.constraints.map(constraint => {
        //         const joints = constraint.joints.map(joint => {
        //             // 连接关节点name
        //             // return joint.joint_1?.name || joint.joint_2?.name || joint.joint_3?.name;

        //             // 加入关节点 xyz property
        //             const jointName = joint.joint_1?.name || joint.joint_2?.name || joint.joint_3?.name;
        //             const property = joint.joint_1?.property || joint.joint_2?.property || joint.joint_3?.property;

        //             // 如果 property 存在且不为 "a"，则拼接 name 和 property
        //             // if (property && property !== "a") {
        //             //     return `${jointName}-${property}`;
        //             // }
        //             // return jointName; // 否则只返回 name

        //             // 简写 jointName
        //             const simplifiedName = jointName
        //                 .replace(/left/gi, 'l') // 将 left 替换为 l
        //                 .replace(/right/gi, 'r'); // 将 right 替换为 r

        //             // 如果 property 存在且不为 "a"，则拼接 simplifiedName 和 property
        //             if (property && property !== "a") {
        //                 return `${simplifiedName}-${property}`;
        //             }
        //             return simplifiedName; // 否则只返回 simplifiedName
        //         }).filter(Boolean); // 过滤掉 undefined

        //         // return `${constraint.type}: ${joints.join(' ~ ')}`;
        //         // 返回包含 title、leftData 和 rightData 的对象

        //         // 计算 leftData 和 rightData
        //         const leftData = this.calculateLeftData(constraint);

        //         return {
        //             title: `${constraint.type}: ${joints.join(' ~ ')}`, // 标题
        //             leftData: leftData, // 左边数据，可以根据实际需求修改
        //             rightData: '35.1°' // 右边数据，可以根据实际需求修改
        //         };
        //     });
        // },
        // 启动compare播放帧监听
        startCompareFrameListener() {
            if (this.compare_frameUpdateInterval) return;
            
            const fps = 100;
            this.compare_frameUpdateInterval = setInterval(() => {
                if (this.app?.viewer1) {
                    // 主动获取当前帧并更新响应式数据
                    this.compare_currentLeftFrame = this.app.viewer1.getCurrentFrame();
                    // console.log("compare_currentLeftFrame", this.compare_currentLeftFrame);
                }
                if (this.app?.viewer2) {
                    // 主动获取当前帧并更新响应式数据
                    this.compare_currentRightFrame = this.app.viewer2.getCurrentFrame();
                    // console.log("compare_currentRightFrame", this.compare_currentRightFrame);
                }
            }, 1000 / fps); // 按帧率更新
        },

        // 停止compare播放帧监听
        stopCompareFrameListener() {
            clearInterval(this.compare_frameUpdateInterval);
            this.compare_frameUpdateInterval = null;
        },

        // 启动display播放帧监听
        startDisplayFrameListener() {
            if (this.display_frameUpdateInterval) return;

            const fps = 100;
            this.display_frameUpdateInterval = setInterval(() => {
                if (this.app?.viewer) {
                    // 主动获取当前帧并更新响应式数据
                    this.display_currentFrame = this.app.viewer.getCurrentFrame();
                    // console.log("display_currentFrame", this.display_currentFrame);
                }

            }, 1000 / fps); // 按帧率更新
        },

        // 停止display播放帧监听
        stopDisplayFrameListener() {
            clearInterval(this.display_frameUpdateInterval);
            this.display_frameUpdateInterval = null;
        },

        initChart(item) {
            const ctx = this.$refs['display-chart-' + item.id];
            if (!ctx) return;

            // 提取纵轴数据（ text 的最后一个单词是纵轴数据）
            const yAxisLabel = item.text.split(' ').pop();

            // 横轴是时间，纵轴是某种类型
            // const timeData = getDisplayTimeData(item); // 时间轴数据
            // const valueData = [10, 20, 15, 25, 30, 20]; // 纵轴数据

            // 关键时间点（假设在时间轴的第 2 和第 4 秒处绘制虚线）
            // const criticalTimes = [2, 4];

            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    // labels: timeData.map(t => `${t}s`), // 横轴标签
                    labels: this.display_frameData, // 横轴标签
                    datasets: [
                        {
                        label: yAxisLabel,
                        data: this.display_chartData[parseInt(item.id)],
                        borderColor: '#000000', // 折线颜色
                        borderWidth: 2,
                        fill: false, // 不填充区域
                        },
                    ],
                },
                options: {
                    scales: {
                        x: {
                            type: 'linear',
                            position: 'bottom',
                            display: true,
                            ticks: {
                                display: false, // 不显示横轴刻度
                            },
                            grid: {
                                display: false, // 不显示横轴网格线
                            },
                            title: {
                                display: true,
                                text: 'time', // x 轴名称
                                color: '#000000',
                                font: { size: 12 },
                            },
                            min: 0,
                            // max: 5.5, // 扩展 x 轴范围
                            // offset: false, // 关闭标签偏移
                        },
                        y: {
                            display: true, // 显示纵轴
                            ticks: {
                                display: false, // 不显示纵轴刻度
                            },
                            grid: {
                                display: false, // 不显示纵轴网格线
                            },
                            title: {
                                display: true,
                                text: yAxisLabel, // y 轴名称
                                color: '#000000',
                                font: { size: 12 },
                            },
                            min: 0,
                            // max: 35, // 扩展 y 轴范围
                            // offset: false, // 关闭标签偏移
                        },
                    },
                    // layout: {
                    //     padding: {
                    //     left: 20,  // 左侧边距（显示 y 轴左侧斜线）
                    //     right: 20, // 右侧边距
                    //     top: 20,   // 顶部边距
                    //     bottom: 20,// 底部边距（显示 x 轴下方斜线）
                    //     },
                    // },
                    plugins: {
                        annotation: {
                            annotations: [
                                ...this.display_criticalFrames.map((time) => ({
                                    type: 'line',
                                    mode: 'vertical',
                                    scaleID: 'x',
                                    value: time,
                                    borderColor: '#C59CF4', // 虚线颜色
                                    borderWidth: 1,
                                    borderDash: [5, 5], // 虚线样式
                                    // 可附加条件：仅当数据存在时显示
                                    drawTime: 'afterDatasetsDraw', // 在数据绘制后渲染
                                    // label: {
                                    //     content: time.toString(), // 直接显示display_criticalFrames中的值
                                    //     enabled: true,
                                    //     position: 'bottom',
                                    //     // backgroundColor: 'rgba(0,0,0,0)',
                                    //     color: '#000000',
                                    //     font: {
                                    //         size: 10,
                                    //         weight: 'bold'
                                    //     },
                                    //     // xAdjust: 0,
                                    //     yAdjust: -10,
                                    // }
                                })),

                                // // x 轴箭头（向右）
                                // {
                                //     type: 'line',
                                //     mode: 'horizontal',
                                //     scaleID: 'x',
                                //     borderColor: '#000000',
                                //     borderWidth: 2,
                                //     xMin: 5,  // 起点为数据最大值
                                //     xMax: 5.5, // 终点为扩展后的轴末端
                                //     yMin: 0,
                                //     yMax: 0,
                                // },
                                // {
                                //     type: 'line',
                                //     borderColor: '#000000',
                                //     borderWidth: 2,
                                //     xMin: 5.35,
                                //     xMax: 5.5,
                                //     yMin: -0.2,
                                //     yMax: 0,
                                //     xScaleID: 'x',
                                //     yScaleID: 'y',
                                // },
                                // {
                                //     type: 'line',
                                //     borderColor: '#000000',
                                //     borderWidth: 2,
                                //     xMin: 5.35,
                                //     xMax: 5.5,
                                //     yMin: 0.2,
                                //     yMax: 0,
                                // },

                                // // y 轴箭头（向上）
                                // {
                                //     type: 'line',
                                //     mode: 'vertical',
                                //     scaleID: 'y',
                                //     borderColor: '#000000',
                                //     borderWidth: 2,
                                //     xMin: 0,
                                //     xMax: 0,
                                //     yMin: 30, // 起点为数据最大值
                                //     yMax: 35, // 终点为扩展后的轴末端
                                // },
                                // {
                                //     type: 'line',
                                //     borderColor: '#000000',
                                //     borderWidth: 2,
                                //     xMin: -0.2,
                                //     xMax: 0,
                                //     yMin: 34,
                                //     yMax: 35,
                                //     xScaleID: 'x',
                                //     yScaleID: 'y',
                                // },
                                // {
                                //     type: 'line',
                                //     borderColor: '#000000',
                                //     borderWidth: 2,
                                //     xMin: 0.2,
                                //     xMax: 0,
                                //     yMin: 34,
                                //     yMax: 35,
                                // },
                            ],
                        },
                        legend: {
                            display: false, // 隐藏图例（数据集标签）
                        },
                    },
                    elements: {
                        point: {
                        radius: 0, // 不显示数据点
                        },
                    },
                    responsive: true,
                    maintainAspectRatio: false,
                },
            });

            ctx.chart = chart; // 将chart对象存储到组件实例中
        },

        calculateDisplayChartData(displayPosition) {
            this.displayData.forEach((item, index) => {
                if (displayPosition.length === 0) {
                    return null;
                }
                
                // 获取constraint中的type
                const type = item.type;

                // 根据type获取对应的leftData
                if (type === 'distance') {
                    const point1 = item.joints[0].joint_1.name;
                    const point2 = item.joints[1].joint_2.name;
                    const property = item.joints[0].joint_1.property;
                    console.log("point1", point1, "point2", point2, "property", property);

                    if (property === 'a' && point1 !== 'ground' && point2 !== 'ground') {
                        const point1_data = displayPosition.find(position => position.name === point1);
                        const point2_data = displayPosition.find(position => position.name === point2);
                        console.log("point1_data", point1_data, "point2_data", point2_data);
                        if (point1_data && point2_data) {
                            // 获取最大帧数（假设x,y,z数组长度相同）
                            const frameCount = point1_data.x.length;
                            console.log("point1_data", point1_data, "point2_data", point2_data);

                            // 计算每一帧的距离
                            const distances = Array.from({ length: frameCount }, (_, frame) => {
                                const dx = point2_data.x[frame] - point1_data.x[frame];
                                const dy = point2_data.y[frame] - point1_data.y[frame];
                                const dz = point2_data.z[frame] - point1_data.z[frame];
                                return Math.sqrt(dx*dx + dy*dy + dz*dz).toFixed(2);
                            });
                            
                            console.log("距离数组:", distances);
                            this.display_chartData[index] = distances;
                        }
                    } 
                    else if (property === 'x' || property === 'y' || property === 'z') {
                        const point1_data = displayPosition.find(position => position.name === point1);
                        const point2_data = displayPosition.find(position => position.name === point2);
                        if (point1_data && point2_data) {
                            console.log("point1_data", point1_data, "point2_data", point2_data);

                            const frameCount = point1_data[property].length; // 获取总帧数
                            const axis = property; // 保存当前计算的坐标轴
                            
                            // 计算所有帧的坐标差值
                            const diffs = Array.from({ length: frameCount }, (_, frame) => {
                                const val1 = point1_data[axis][frame];
                                const val2 = point2_data[axis][frame];
                                return Math.abs(val2 - val1).toFixed(2);
                            });
                            
                            console.log(`${axis}轴差值数组:`, diffs);
                            this.display_chartData[index] = diffs;
                        }
                    }
                    else if (point1 === 'ground' || point2 === 'ground') {
                        const point1_data = displayPosition.find(position => position.name === point1);
                        const point2_data = displayPosition.find(position => position.name === point2);
                        if (point1_data && point2_data) {
                            const frameCount = point1_data.y.length; // 使用y轴数据长度
        
                            // 强制计算y轴差值（地面点特殊处理）
                            const yDiffs = Array.from({ length: frameCount }, (_, frame) => {
                                const y1 = point1_data.y[frame];
                                const y2 = point2_data.y[frame];
                                return Math.abs(y2 - y1).toFixed(2);
                            });
                            
                            console.log("地面点y轴差值数组:", yDiffs);
                            this.display_chartData[index] = yDiffs;
                        }
                    }
                }

                else if (type === 'angle') {
                    const point1 = item.joints[0].joint_1.name;
                    const point2 = item.joints[1].joint_2.name;
                    const point3 = item.joints[2].joint_3.name;
                    const point1_property = item.joints[0].joint_1.property;
                    // const point2_property = item.joints[1].joint_2.property;
                    const point3_property = item.joints[2].joint_3.property;

                    console.log("point1", point1, "point2", point2, "point3", point3);

                    // 获取三个节点的坐标
                    const point1_data = displayPosition.find(position => position.name === point1);
                    const point2_data = displayPosition.find(position => position.name === point2);
                    const point3_data = displayPosition.find(position => position.name === point3);

                    // if (point1 !== point2 && point2 !== point3) {
                        if (point1_data && point2_data && point3_data) {
                            // 获取总帧数（取x坐标数组长度）
                            const frameCount = point1_data.x.length;

                            // 计算每一帧的角度
                            const angles = Array.from({ length: frameCount }, (_, frame) => {
                                // 计算向量BA（从point2指向point1）
                                const BA = point1_property === 'a' ? {
                                    x: point1_data.x[frame] - point2_data.x[frame],
                                    y: point1_data.y[frame] - point2_data.y[frame],
                                    z: point1_data.z[frame] - point2_data.z[frame]
                                } : {
                                    x: point1_property === 'x' ? 1 : 0,
                                    y: point1_property === 'y' ? 1 : 0,
                                    z: point1_property === 'z' ? 1 : 0
                                };

                                // 计算向量BC（从point2指向point3）
                                const BC = point3_property === 'a' ? {
                                    x: point3_data.x[frame] - point2_data.x[frame],
                                    y: point3_data.y[frame] - point2_data.y[frame],
                                    z: point3_data.z[frame] - point2_data.z[frame]
                                } : {
                                    x: point3_property === 'x' ? 1 : 0,
                                    y: point3_property === 'y' ? 1 : 0,
                                    z: point3_property === 'z' ? 1 : 0
                                };

                                // 计算点积
                                const dotProduct = BA.x * BC.x + BA.y * BC.y + BA.z * BC.z;

                                // 计算向量模长
                                const magBA = Math.sqrt(BA.x ** 2 + BA.y ** 2 + BA.z ** 2);
                                const magBC = Math.sqrt(BC.x ** 2 + BC.y ** 2 + BC.z ** 2);

                                // 处理除零错误
                                if (magBA === 0 || magBC === 0) return '0.0°';

                                // 计算角度
                                const radians = Math.acos(dotProduct / (magBA * magBC));
                                const degrees = (radians * 180 / Math.PI).toFixed(1);
                                
                                return degrees;
                            });

                            console.log('角度数组:', angles);
                            this.display_chartData[index] = angles;
                        }
                    // }
                    // else if (point1 === point2) {
                        
                    // }
                    // else if (point2 === point3) {
                        
                    // }
                }
            });
        },

        handleCurrentMarkedBoxIdChange(index) {
            this.display_currentMarkedBoxId = index;
        },

        handleAddMarkedBox() {
            this.display_markedFrames.push({
                frame: this.display_currentFrame,
                marked: false,
            });
        },

        handleMarkCurrentFrame(display_currentMarkedBoxId, display_currentFrame) {
            this.display_markedFrames[display_currentMarkedBoxId].marked = true;
            this.display_markedFrames[display_currentMarkedBoxId].frame = display_currentFrame;
        },

        getBodyPartName(body_part) {
            return body_part
                .replace(/left/gi, 'l')
                .replace(/right/gi, 'r');
        },

        FeedbackHighlightKeywords(feedback) {
            // console.log("old_feedback", feedback);
            const body_part = ['head', 'back', 'feet', 'toes', 'knees', 'thighs', 'spine', 'hips'];
            // const advice = ['wide', 'outward', 'ahead', 'inward', 'outer', 'deeper', 'Lift', 'up'];
            
            // 高亮 body_part 关键词（#F7877C 颜色）
            body_part.forEach((word) => {
                const regex = new RegExp(`\\b${word}\\b`, 'gi');
                feedback = feedback.replace(
                    regex,
                    `<span style="color: #F7877C;">${word}</span>`
                );
            });
            // console.log("new_feedback", feedback);
            // 高亮 advice 关键词（#FEBA70 颜色）
            // advice.forEach((word) => {
            //     const regex = new RegExp(`\\b${word}\\b`, 'gi');
            //     feedback = feedback.replace(
            //         regex,
            //         `<span style="color: #FEBA70;">${word}</span>`
            //     );
            // });

            // 使用单词边界匹配，但通过回调函数处理替换
            // const highlight = (text, words, color) => {
            //     const regex = new RegExp(`\\b(${words.join('|')})\\b`, 'gi');
            //     return text.replace(regex, `<span style="color: ${color};">$1</span>`);
            // };

            // feedback = highlight(feedback, body_part, '#F7877C');
            // feedback = highlight(feedback, advice, '#FEBA70');
            return feedback;
        },

        getRelativeConstraintsJoints(joints) {
            const joints_name = joints.map(joint => {
                const jointName = joint.joint_1?.name || joint.joint_2?.name || joint.joint_3?.name;
                const property = joint.joint_1?.property || joint.joint_2?.property || joint.joint_3?.property;
                const simplifiedName = jointName
                    .replace(/left/gi, 'l')
                    .replace(/right/gi, 'r');
                return property && property !== "a" ? `${simplifiedName}-${property}` : simplifiedName;
            }).filter(Boolean);

            return `${joints_name.join(' ~ ')}`;
        },

        isVisualizationOptionActive(VisualizationAttribute, option) {
            return VisualizationAttribute === option;
        },
    },
    computed: {
        currentImage() {
            return `${this.currentIndex <= this.ori_segs[1].frame + 5 ? this.basePath_ori_zh : this.basePath_ori_ce}${this.currentIndex.toString().padStart(4, '0')}.png`;
        },
        getMarkStyle(){
            return (feedback, id) => {
                var pos;
                const frame = this.currentRefIndex[id] + this.ref_segs[id].frame - 1;
                if (this.currentRefView[id]) {
                    pos = this.refKeyPoints_zh[frame][feedback.body_part[0]];
                }else {
                    pos = this.refKeyPoints_ce[frame][feedback.body_part[0]];
                }
                return {
                    left: `${pos.x * 0.6}px`,
                    top: `${pos.y * 0.65}px`
                };
            };
        },
        getAnimationMarkStyle(){
            return (body_part, frame) => {
                var pos;
                pos = this.oriKeyPoints_ce[frame - 1][body_part];
                return {
                    left: `${pos.x * 0.6}px`,
                    top: `${pos.y * 0.68}px`
                };
            };
        },
        getAbsolutePosition(){
            return (body_part, frame) => {
                var pos;
                pos = this.oriKeyPoints_ce[frame - 1][body_part];
                const width = 1198.760;
                const height = 742.213;
                return {
                    x: pos.x * 0.6 + width / 100 * (frame / this.screenFrames * 100 - 60),
                    y: pos.y * 0.68 - height * 0.05
                };
            };
        },
        SmoothPath_y(){
            return (body_part, L, R) => {
                var path = "";
                const width = 1198.760;
                const height = 742.213;
                for (var i = L; i < R; i++) {
                    var pos = this.oriKeyPoints_ce[i][body_part];
                    if (path === "") {
                        path +=`M ${pos.x * 0.6 + width / 100 * (i / this.screenFrames * 100 - 20 * i / R - 40)} ${pos.y * 0.7 + height / 100 * (-30 + i / R * 25)}`;
                    }else {
                        path+=` L ${pos.x * 0.6 + width / 100 * (i / this.screenFrames * 100 - 20 * i / R - 40)} ${pos.y * 0.7 + height / 100 * (-30 + i / R * 25)}`;
                    }
                }
                return path;
            };
        },
        SmoothPath_x(){
            return (body_part, L, R) => {
                var path = "";
                const width = 1198.760;
                const height = 742.213;
                for (var i = L; i < R; i++) {
                    var pos = this.oriKeyPoints_ce[i][body_part];
                    if (path === "") {
                        path +=`M ${pos.x * 0.6 + width / 100 * (i / this.screenFrames * 100 - 60)} ${pos.y * 0.7 - height * 0.05}`;
                    }else {
                        path+=` L ${pos.x * 0.6 + width / 100 * (i / this.screenFrames * 100 - 60)} ${pos.y * 0.7 - height * 0.05}`;
                    }
                }
                return path;
            };
        },
        comparisonData() {
            if (!this.isCompareDataLoaded) return []; // 数据未加载时返回空
            
            // const currentLeftFrame = this.app.viewer1.getCurrentFrame();
            // const currentRightFrame = this.app.viewer2.getCurrentFrame();
            // 获取当前correction view选中的segment
            // this.correctionSelectedSegment = localStorage.getItem('selectedNumber');

            const leftFrame = this.compare_currentLeftFrame;
            const rightFrame = this.compare_currentRightFrame;

            // 获取当前选中的 assessment
            const selectedAssessment = assessmentRef.assessment.find(
                assessment => assessment.id === this.correctionSelectedSegment.toString()
            );

            if (!selectedAssessment || !selectedAssessment.constraints) {
                return []; // 如果没有 constraints，返回空数组
            }

            // 遍历 constraints，生成 title
            // return selectedAssessment.constraints.map(constraint => {
            //     const joints = Object.values(constraint.joints).map(joint => {
            //         return joint.name || joint.joint_1?.name || joint.joint_2?.name || joint.joint_3?.name;
            //     }).filter(Boolean); // 过滤掉 undefined

            //     return `${constraint.type}: ${joints.join(' ~ ')}`;
            // });

            // 遍历 constraints，生成包含 title、leftData 和 rightData 的对象
            return selectedAssessment.constraints
                .filter(constraint => constraint.type !== 'trajectory') // 过滤掉 type 为 trajectory 的 constraint
                .map(constraint => {
                const joints = constraint.joints.map(joint => {
                    // 连接关节点name
                    // return joint.joint_1?.name || joint.joint_2?.name || joint.joint_3?.name;

                    // 加入关节点 xyz property
                    const jointName = joint.joint_1?.name || joint.joint_2?.name || joint.joint_3?.name;
                    const property = joint.joint_1?.property || joint.joint_2?.property || joint.joint_3?.property;

                    // 如果 property 存在且不为 "a"，则拼接 name 和 property
                    // if (property && property !== "a") {
                    //     return `${jointName}-${property}`;
                    // }
                    // return jointName; // 否则只返回 name

                    // 简写 jointName
                    const simplifiedName = jointName
                        .replace(/left/gi, 'l') // 将 left 替换为 l
                        .replace(/right/gi, 'r'); // 将 right 替换为 r

                    // 如果 property 存在且不为 "a"，则拼接 simplifiedName 和 property
                    if (property && property !== "a") {
                        return `${simplifiedName}-${property}`;
                    }
                    return simplifiedName; // 否则只返回 simplifiedName
                }).filter(Boolean); // 过滤掉 undefined

                // return `${constraint.type}: ${joints.join(' ~ ')}`;
                // 返回包含 title、leftData 和 rightData 的对象

                // 计算 leftData 和 rightData
                const leftData = this.calculateCompareData(constraint, leftFrame, this.compare_leftPosition);
                const rightData = this.calculateCompareData(constraint, rightFrame, this.compare_rightPosition);

                return {
                    title: `${constraint.type}: ${joints.join(' ~ ')}`, // 标题
                    leftData: leftData, // 左边数据，可以根据实际需求修改
                    rightData: rightData // 右边数据，可以根据实际需求修改
                };
            });
        },
    }
};

class AppD {
	constructor(el, location, vueInstance) {
		const hash = location.hash ? queryString.parse(location.hash) : {};
		this.options = {
			kiosk: Boolean(hash.kiosk),
			model: hash.model || '',
			preset: hash.preset || '',
			cameraPosition: hash.cameraPosition ? hash.cameraPosition.split(',').map(Number) : null,
		};

		this.el = el;
        this.vueInstance = vueInstance; // 保存 Vue 组件实例
		this.viewer = null;
		this.viewerEl = null;

		const options = this.options;
		if (options.kiosk) {
			const headerEl = document.querySelector('header');
			headerEl.style.display = 'none';
		}
		if (options.model) {
			this.view(options.model, '', new Map());
		}

		this.view();
	}
	createViewer() {
		this.viewerEl = document.createElement('div');
		this.el.appendChild(this.viewerEl);
		this.viewer = new ViewerD(this.viewerEl, this.options, 24);
        this.viewer.loadVideo("/ref.mp4");
		return this.viewer;
	}
	view() {
		if (this.viewer) this.viewer.clear();
		const viewer = this.viewer || this.createViewer();
        // 取display的数据
        // 使用 Promise.all 确保数据模型加载完成
        const display_loadPromise = Promise.all([
            new Promise(resolve => {
                const dataParser = new DataParser();
                dataParser.load("/ori_data.glb").then(() => {
                    // 获取某个节点的数据长度（例如 'head' 节点）
                    const headXData = dataParser.getPositionByName('head', 0);
                    console.log("headData", headXData);
                    const frameCount = headXData.length; // 根据 x 数组的长度确定帧数

                    this.vueInstance.display_frameData = dataParser.getFrameData();

                    this.vueInstance.display_position = [
                        {
                            name: 'head',
                            x: dataParser.getPositionByName('head', 0),
                            y: dataParser.getPositionByName('head', 1),
                            z: dataParser.getPositionByName('head', 2),
                        },
                        {
                            name: 'neck',
                            x: dataParser.getPositionByName('neck', 0),
                            y: dataParser.getPositionByName('neck', 1),
                            z: dataParser.getPositionByName('neck', 2),
                        },
                        {
                            name: 'right_elbow',
                            x: dataParser.getPositionByName('right_elbow', 0),
                            y: dataParser.getPositionByName('right_elbow', 1),
                            z: dataParser.getPositionByName('right_elbow', 2),
                        },
                        {
                            name: 'right_wrist',
                            x: dataParser.getPositionByName('right_wrist', 0),
                            y: dataParser.getPositionByName('right_wrist', 1),
                            z: dataParser.getPositionByName('right_wrist', 2),
                        },
                        {
                            name: 'left_elbow',
                            x: dataParser.getPositionByName('left_elbow', 0),
                            y: dataParser.getPositionByName('left_elbow', 1),
                            z: dataParser.getPositionByName('left_elbow', 2),
                        },
                        {
                            name: 'left_wrist',
                            x: dataParser.getPositionByName('left_wrist', 0),
                            y: dataParser.getPositionByName('left_wrist', 1),
                            z: dataParser.getPositionByName('left_wrist', 2),
                        },
                        {
                            name: 'hip',
                            x: dataParser.getPositionByName('hip', 0),
                            y: dataParser.getPositionByName('hip', 1),
                            z: dataParser.getPositionByName('hip', 2),
                        },
                        {
                            name: 'right_knee',
                            x: dataParser.getPositionByName('right_knee', 0),
                            y: dataParser.getPositionByName('right_knee', 1),
                            z: dataParser.getPositionByName('right_knee', 2),
                        },
                        {
                            name: 'right_ankle',
                            x: dataParser.getPositionByName('right_ankle', 0),
                            y: dataParser.getPositionByName('right_ankle', 1),
                            z: dataParser.getPositionByName('right_ankle', 2),
                        },
                        {
                            name: 'left_knee',
                            x: dataParser.getPositionByName('left_knee', 0),
                            y: dataParser.getPositionByName('left_knee', 1),
                            z: dataParser.getPositionByName('left_knee', 2),
                        },
                        {
                            name: 'left_ankle',
                            x: dataParser.getPositionByName('left_ankle', 0),
                            y: dataParser.getPositionByName('left_ankle', 1),
                            z: dataParser.getPositionByName('left_ankle', 2),
                        },
                        {
                            name: 'ground',
                            x: new Array(frameCount).fill(0), // x 数组均为 0
                            y: new Array(frameCount).fill(0), // y 数组均为 0
                            z: new Array(frameCount).fill(0), // z 数组均为 0
                        },
                    ];
                    
                    console.log("display_position", this.vueInstance.display_position);
                    console.log("Left data loaded");
                    resolve();
                });
                // dataParser.clear();
            }),
        ]);

        // 全部加载完成后更新状态
        display_loadPromise.then(() => {
            this.vueInstance.isDisplayDataLoaded = true;
            console.log("All data loaded");
        });
		viewer.load("/ref.glb").then(() => {
			const keyFrames = [0, 62, 91, 123];
			viewer.setKeyFrames(keyFrames);
			viewer.setKeyFrame(0);
            // console.log(this.viewer.getAngle(190, 193));
		});
	}
}

class AppC {
	constructor(el, location, vueInstance) {
		const hash = location.hash ? queryString.parse(location.hash) : {};
		this.options = {
			kiosk: Boolean(hash.kiosk),
			model: hash.model || '',
			preset: hash.preset || '',
			cameraPosition: hash.cameraPosition ? hash.cameraPosition.split(',').map(Number) : null,
		};

		this.el = el;
        this.vueInstance = vueInstance; // 保存 Vue 组件实例

		this.viewer1 = null;
		this.viewerEl1 = null;
		this.viewer2 = null;
		this.viewerEl2 = null;

		const options = this.options;
		if (options.kiosk) {
			const headerEl = document.querySelector('header');
			headerEl.style.display = 'none';
		}
		if (options.model) {
			this.view(options.model, '', new Map());
		}

		this.view();
	}

	createViewer() {
		this.viewerEl1 = document.createElement('div');
		this.viewerEl1.style.cssText = `
            flex: 1;
            height: 100%; 
            position: relative;
            z-index: 0;
		`;
		this.el.appendChild(this.viewerEl1);
		this.viewerEl2 = document.createElement('div');
		this.viewerEl2.style.cssText = `
            flex: 1;
            height: 100%; 
            position: relative;
            z-index: 0;
		`;
		this.el.appendChild(this.viewerEl2);
        this.viewer1 = new ViewerC(this.viewerEl1, this.options, 24);
		this.viewer2 = new ViewerC(this.viewerEl2, this.options, 30);
	}
	view() {
		if (this.viewer1) {
			this.viewer1.clear();
		}
		if (this.viewer2) {
			this.viewer2.clear();
		}

		this.createViewer();
        // 取ori和ref的数据
        // 使用 Promise.all 确保两个模型都加载完成
        const loadPromise = Promise.all([
            new Promise(resolve => {
                const leftDataParser = new DataParser();
                leftDataParser.load("/ori_data.glb").then(() => {
                    // this.compare_leftPosition = [
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('head'), 0),
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('neck'), 0),
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('right_elbow'), 0),
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('right_wrist'), 0),
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('left_elbow'), 0),
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('left_wrist'), 0),
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('hip'), 0),
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('right_knee'), 0),
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('right_ankle'), 0),
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('left_knee'), 0),
                    //     leftDataParser.getPosition(this.getIndexByJointnameForDistance('left_ankle'), 0),
                    // ];
                    // 获取某个节点的数据长度（例如 'head' 节点）
                    const headXData = leftDataParser.getPositionByName('head', 0);
                    console.log("headData", headXData);
                    const frameCount = headXData.length; // 根据 x 数组的长度确定帧数

                    this.vueInstance.compare_leftPosition = [
                        {
                            name: 'head',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('head'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('head'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('head'), 2),
                            x: leftDataParser.getPositionByName('head', 0),
                            y: leftDataParser.getPositionByName('head', 1),
                            z: leftDataParser.getPositionByName('head', 2),
                        },
                        {
                            name: 'neck',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('neck'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('neck'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('neck'), 2),
                            x: leftDataParser.getPositionByName('neck', 0),
                            y: leftDataParser.getPositionByName('neck', 1),
                            z: leftDataParser.getPositionByName('neck', 2),
                        },
                        {
                            name: 'right_elbow',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_elbow'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_elbow'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_elbow'), 2),
                            x: leftDataParser.getPositionByName('right_elbow', 0),
                            y: leftDataParser.getPositionByName('right_elbow', 1),
                            z: leftDataParser.getPositionByName('right_elbow', 2),
                        },
                        {
                            name: 'right_wrist',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_wrist'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_wrist'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_wrist'), 2),
                            x: leftDataParser.getPositionByName('right_wrist', 0),
                            y: leftDataParser.getPositionByName('right_wrist', 1),
                            z: leftDataParser.getPositionByName('right_wrist', 2),
                        },
                        {
                            name: 'left_elbow',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_elbow'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_elbow'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_elbow'), 2),
                            x: leftDataParser.getPositionByName('left_elbow', 0),
                            y: leftDataParser.getPositionByName('left_elbow', 1),
                            z: leftDataParser.getPositionByName('left_elbow', 2),
                        },
                        {
                            name: 'left_wrist',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_wrist'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_wrist'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_wrist'), 2),
                            x: leftDataParser.getPositionByName('left_wrist', 0),
                            y: leftDataParser.getPositionByName('left_wrist', 1),
                            z: leftDataParser.getPositionByName('left_wrist', 2),
                        },
                        {
                            name: 'hip',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('hip'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('hip'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('hip'), 2),
                            x: leftDataParser.getPositionByName('hip', 0),
                            y: leftDataParser.getPositionByName('hip', 1),
                            z: leftDataParser.getPositionByName('hip', 2),
                        },
                        {
                            name: 'right_knee',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_knee'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_knee'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_knee'), 2),
                            x: leftDataParser.getPositionByName('right_knee', 0),
                            y: leftDataParser.getPositionByName('right_knee', 1),
                            z: leftDataParser.getPositionByName('right_knee', 2),
                        },
                        {
                            name: 'right_ankle',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_ankle'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_ankle'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('right_ankle'), 2),
                            x: leftDataParser.getPositionByName('right_ankle', 0),
                            y: leftDataParser.getPositionByName('right_ankle', 1),
                            z: leftDataParser.getPositionByName('right_ankle', 2),
                        },
                        {
                            name: 'left_knee',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_knee'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_knee'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_knee'), 2),
                            x: leftDataParser.getPositionByName('left_knee', 0),
                            y: leftDataParser.getPositionByName('left_knee', 1),
                            z: leftDataParser.getPositionByName('left_knee', 2),
                        },
                        {
                            name: 'left_ankle',
                            // x: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_ankle'), 0),
                            // y: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_ankle'), 1),
                            // z: leftDataParser.getPosition(this.vueInstance.getIndexByJointnameForOriDistance('left_ankle'), 2),
                            x: leftDataParser.getPositionByName('left_ankle', 0),
                            y: leftDataParser.getPositionByName('left_ankle', 1),
                            z: leftDataParser.getPositionByName('left_ankle', 2),
                        },
                        {
                            name: 'ground',
                            x: new Array(frameCount).fill(0), // x 数组均为 0
                            y: new Array(frameCount).fill(0), // y 数组均为 0
                            z: new Array(frameCount).fill(0), // z 数组均为 0
                        },
                    ];
                    console.log("compare_leftPosition", this.vueInstance.compare_leftPosition);
                    console.log("Left data loaded");
                    resolve();
                });
                // leftDataParser.clear();
            }),
            new Promise(resolve => {
                const rightDataParser = new DataParser();
                rightDataParser.load("/ref_data.glb").then(() => {
                    // 获取某个节点的数据长度（例如 'head' 节点）
                    const headXData = rightDataParser.getPositionByName('head', 0);
                    const frameCount = headXData.length; // 根据 x 数组的长度确定帧数

                    this.vueInstance.compare_rightPosition = [
                        {
                            name: 'head',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('head'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('head'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('head'), 2),
                            x: rightDataParser.getPositionByName('head', 0),
                            y: rightDataParser.getPositionByName('head', 1),
                            z: rightDataParser.getPositionByName('head', 2),
                        },
                        {
                            name: 'neck',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('neck'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('neck'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('neck'), 2),
                            x: rightDataParser.getPositionByName('neck', 0),
                            y: rightDataParser.getPositionByName('neck', 1),
                            z: rightDataParser.getPositionByName('neck', 2),
                        },
                        {
                            name: 'right_elbow',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_elbow'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_elbow'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_elbow'), 2),
                            x: rightDataParser.getPositionByName('right_elbow', 0),
                            y: rightDataParser.getPositionByName('right_elbow', 1),
                            z: rightDataParser.getPositionByName('right_elbow', 2),
                        },
                        {
                            name: 'right_wrist',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_wrist'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_wrist'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_wrist'), 2),
                            x: rightDataParser.getPositionByName('right_wrist', 0),
                            y: rightDataParser.getPositionByName('right_wrist', 1),
                            z: rightDataParser.getPositionByName('right_wrist', 2),
                        },
                        {
                            name: 'left_elbow',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_elbow'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_elbow'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_elbow'), 2),
                            x: rightDataParser.getPositionByName('left_elbow', 0),
                            y: rightDataParser.getPositionByName('left_elbow', 1),
                            z: rightDataParser.getPositionByName('left_elbow', 2),
                        },
                        {
                            name: 'left_wrist',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_wrist'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_wrist'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_wrist'), 2),
                            x: rightDataParser.getPositionByName('left_wrist', 0),
                            y: rightDataParser.getPositionByName('left_wrist', 1),
                            z: rightDataParser.getPositionByName('left_wrist', 2),
                        },
                        {
                            name: 'hip',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('hip'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('hip'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('hip'), 2),
                            x: rightDataParser.getPositionByName('hip', 0),
                            y: rightDataParser.getPositionByName('hip', 1),
                            z: rightDataParser.getPositionByName('hip', 2),
                        },
                        {
                            name: 'right_knee',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_knee'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_knee'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_knee'), 2),
                            x: rightDataParser.getPositionByName('right_knee', 0),
                            y: rightDataParser.getPositionByName('right_knee', 1),
                            z: rightDataParser.getPositionByName('right_knee', 2),
                        },
                        {
                            name: 'right_ankle',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_ankle'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_ankle'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('right_ankle'), 2),
                            x: rightDataParser.getPositionByName('right_ankle', 0),
                            y: rightDataParser.getPositionByName('right_ankle', 1),
                            z: rightDataParser.getPositionByName('right_ankle', 2),
                        },
                        {
                            name: 'left_knee',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_knee'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_knee'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_knee'), 2),
                            x: rightDataParser.getPositionByName('left_knee', 0),
                            y: rightDataParser.getPositionByName('left_knee', 1),
                            z: rightDataParser.getPositionByName('left_knee', 2),
                        },
                        {
                            name: 'left_ankle',
                            // x: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_ankle'), 0),
                            // y: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_ankle'), 1),
                            // z: rightDataParser.getPosition(this.vueInstance.getIndexByJointnameForRefDistance('left_ankle'), 2),
                            x: rightDataParser.getPositionByName('left_ankle', 0),
                            y: rightDataParser.getPositionByName('left_ankle', 1),
                            z: rightDataParser.getPositionByName('left_ankle', 2),
                        },
                        {
                            name: 'ground',
                            x: new Array(frameCount).fill(0), // x 数组均为 0
                            y: new Array(frameCount).fill(0), // y 数组均为 0
                            z: new Array(frameCount).fill(0), // z 数组均为 0
                        },
                    ];
                    console.log("compare_rightPosition", this.vueInstance.compare_rightPosition);
                    console.log("Right data loaded");
                    resolve();
                });
                // rightDataParser.clear();
            })
        ]);

        // 全部加载完成后更新状态
        loadPromise.then(() => {
            this.vueInstance.isCompareDataLoaded = true;
            console.log("All data loaded");
        });
        
		this.viewer1.load("/ori.glb").then(() => {
			const keyFrames = [97, 134, 165];
			this.viewer1.setKeyFrames(keyFrames);
			this.viewer1.setKeyFrame(0);
		});
		this.viewer2.load("/ref.glb").then(() => {
			const keyFrames = [62, 91, 123];
			this.viewer2.setKeyFrames(keyFrames);
			this.viewer2.setKeyFrame(0);
		});
	}
}

</script>

<style scoped>
.container {
    /* 长宽改为1553*799 */
    /* 保持长宽比 1160：812 -> 1553: 799 */
    /* aspect-ratio: 1160 / 812; */
    aspect-ratio: 1553 / 799;
    /* 自适应宽度 */
    /* width: 100%; */
    display: flex;
    flex-direction: column;
    align-items: center;
    /* padding: 5px; 内边距 */
    /* box-sizing: border-box; */
}

.header {
    /* 保持长宽比 1160：39 -> 1553: 39 */
    /* aspect-ratio: 1160 / 39; */
    aspect-ratio: 1553 / 39;
    width: 100%;
    /* height: 4.8%; */
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: #F3F3F3;
}

.ExplorationView-title {
    width: 50%;
    font-size: 20px;
    font-weight: bold;
    
    position: relative;
}

.EditionView-title {
    width: 50%;
    font-size: 20px;
    font-weight: bold;

    position: relative;
}

.ExplorationView-title-icon {
    width: 3%;
    /* height: 1%; */
    object-fit: contain;
}

.EditionView-title-icon {
    width: 3%;
    /* height: 1%; */
    object-fit: contain;
}

/* 默认状态下没有黑色线 */
.ExplorationView-title::after, .EditionView-title::after {
    content: '';
    position: absolute;
    left: 5%;
    bottom: 0;
    width: 90%;
    height: 2px;
    background-color: transparent; /* 初始透明 */
    transition: background-color 0.3s ease;
}

/* 选中状态下显示黑色线 */
.ExplorationView-title.active::after, .EditionView-title.active::after {
    background-color: black;
}

.content-container {
    /* 保持长宽比 1160：773 -> 1553: 760 */
    /* aspect-ratio: 1160 / 773; */
    aspect-ratio: 1553 / 760;
    width: 100%;
    display: flex;
    align-items: center;
    padding: 5px;
    box-sizing: border-box;

    background-color: #FFFFFF;
}

.content-container {
    /* 保持长宽比 1160：773 -> 1553: 760 */
    /* aspect-ratio: 1160 / 773; */
    aspect-ratio: 1553 / 760;
    width: 100%;
    display: flex;
    align-items: center;
    padding: 5px;
    box-sizing: border-box;

    background-color: #FFFFFF;
}

.media-container-display {
    /* 保持长宽比 1216: 730 */
    /* aspect-ratio: 1216 / 730; */
    position: relative;
    width: 78.5%;
    height: 100%;
    display: flex; /* 启用flex布局 */
    align-items: center;
}

.media-container-compare {
    /* 保持长宽比 1216: 730 */
    /* aspect-ratio: 1216 / 730; */
    position: relative;
    width: 78.5%;
    height: 100%;
    display: flex;
    align-items: center;
}

.media-container{
    /* 保持长宽比 1216: 730 */
    /* aspect-ratio: 1216 / 730; */
    position: relative;
    width: 78.5%;
    height: 100%;
    display: flex;
    align-items: center;
    overflow: scroll;
}

.ref-frame {
  position: absolute;
  top: 0;
  width: 100%;      /* 继承父容器宽度 */
  height: 24%;     /* 继承父容器高度 */
  z-index: 3;

  display: flex;
  justify-content: center; /* 水平居中 */
  pointer-events: none; /* 禁止鼠标事件 */
}

.frame-number {
    width: 25px;
    height: 25px;
    font-size: larger;
    border-radius: 50%;
    border: 5px solid #A3A3A3;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    position: absolute;
    bottom: 0;
    pointer-events: auto; /* 允许鼠标事件 */

    background-color: #FFFFFF;

    z-index: 5;
}

.frame-number.active {
    border: 5px solid #C59CF4;
}

.frame-control {
    position: absolute;
    bottom: 50px;
    left: 44%;
}

.frame-control-svg {
    position: absolute;
    top: 0;
    left: 0;
    /* z-index: 0; */
    pointer-events: none; /* 允许点击事件穿透到 frame-number */
}

.frame-control-play{
    width: 30px;
    height: 30px;
    cursor: pointer;
    pointer-events: auto; /* 允许鼠标事件 */
    position: absolute;
    bottom: 20px;
    left: 55px;
}

.frame-control-rotate{
    width: 30px;
    height: 30px;
    cursor: pointer;
    pointer-events: auto; /* 允许鼠标事件 */
    position: absolute;
    bottom: 20px;
    left: 0
}

.frame-problem {
    border: 3px solid #E8EBF0;
    border-radius: 5px;
    height: 90px;
    width: 280px;
    display: flex; /* 保持弹性布局 */
    position: absolute;
    bottom: 20px;
    z-index: 4;
    pointer-events: auto; /* 允许鼠标事件 */
    cursor: pointer;
}

.frame-problem-icon {
    height: 90px; /* 强制正方形 */
    object-fit: cover; /* 保持图片比例 */
}

.frame-problem-text {
    flex: 1; /* 占据剩余空间 */
    padding: 8px;
    font-size: 1.0em;
    color: #2E4051;
    display: flex;
    justify-content: center; /* 垂直居中 */
    align-items: center; /* 水平居中 */
    text-align: left;
    margin-left: 5px;
}

.correct-frame {
    position: absolute;
    top: 15px;
    left: 200px;
    width: 430px;
    height: 530px;
    z-index: 5;
    cursor: pointer;
    border: 4px solid #E8EBF0;
    background-color: white;
    color: white;
}

.correct-frame-menu {
    position: absolute;
    left: 3%;
    width: 50px;
    color: black;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: transparent;
    z-index: 6;
    border: 2px solid #E8EBF0;
    border-radius: 8px;
    padding: 2%;
}

.correct-frame-menu-title{
    border-bottom: 4px solid #E8EBF0;
    padding-bottom: 10%;
    top: 0;
    font-size: 1.2em;
    font-weight: 600;
}

.correct-frame-menu-item {
    width: 100%;
    height: 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    pointer-events: all;
    font-size: 0.8em;
    padding: 5%;
    margin: 1%;
}

.correct-frame-menu-item.active {
    background-color: #C59CF4;
    color: white;
}

.correct-frame-menu-item img{
    width: 60%;
    padding: 10%;
}

.correct-frame-image {
    height: 120%;
    left: -70%;
    top: -20%;
    object-fit: contain;
    position: absolute;
}

.correct-frame-feedback {
    position: absolute;
    left: 25%;
    top: 3%;
    width: 75%;
    height: 20%;
    color: black;
    font-size: 1.2em;
    text-align: left;
}

.progress-bar-svg {
    position: absolute;
    bottom: 0;
}

.animation-button {
    /* position: absolute; */
    /* height: 5%; */
    object-fit: contain;
    z-index: 3;
    cursor: pointer;
    /* bottom: 1%; */
    /* left: 45%; */

    /* position: sticky; */
    /* bottom: 1%; */
    position: fixed;
    height: 3.4%;
    left: 46%;
    top: 70%;
    /* transform: translateX(-50%); */
}

.animation-scale {
    /* position: absolute; */
    /* height: 5%; */
    object-fit: contain;
    z-index: 3;
    cursor: pointer;
    /* bottom: 1%; */
    /* left: 80%; */

    position: fixed;
    height: 3.4%;
    left: 67%;
    top: 70%;
    /* transform: translateX(-50%); */
}

.animation-container {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: contain; /* 保持比例完整显示 */
  transition: transform 0.1s;
  z-index: 2;
}

.animation-container img {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 保持比例完整显示 */
}

.background-container {
    position: absolute;
    width: 100%;
    height: 100%;
    object-fit: contain;
    z-index: 1;
}

.stacked-background {
    width: 100%;
    height: 100%;
    object-fit: contain;
    z-index: 1;
}

.background-mark {
    position: absolute;
    width: 50px;
    height: 30px;
    background: transparent;
    border: 3px dashed #F7877C; 
}

.animation-mark {
    position: absolute;
    width: 20px;
    height: 20px;
    background: white;
    border: 4px solid #F7877C;
    border-radius: 50%;
}

.animation-mark-traj {
    position: absolute;
    width: 6px;
    height: 6px;
    background: #FEBA70;
    border-radius: 50%;
    z-index: 6;
}

.animation-svg {
    z-index: 4;
    pointer-events: none;
}

.background-mark-number {
    position: absolute;
    width: 20px;
    height: 20px;
    background: #F7877C;
    border-radius: 50%;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1em;
    top: -12px;
    right: -12px;
}

.control-container {
    /* 保持长宽比 313: 730 */
    /* aspect-ratio: 313 / 730; */
    width: 21.2%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #F3F3F3;
}

.control-nav {
    /* 保持长宽比 313: 34 */
    /* aspect-ratio: 313 / 34; */
    width: 100%;
    height: 4.65%;
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: #FFFFFF;
}

.display-button, .compare-button {
    width: 50%;
    height: 100%;
    /* 居中显示 */
    display: flex;
    justify-content: center;
    align-items: center;
    /* font-size: 0.8em; */
    font-size: 17px;
    font-weight: bold;
    transition: background-color 0.3s;

    position: relative;
}

/* 默认状态下没有黑色线 */
.display-button::after, .compare-button::after {
    content: '';
    position: absolute;
    left: 5%;
    bottom: 0;
    width: 90%;
    height: 2px;
    background-color: transparent; /* 初始透明 */
    transition: background-color 0.3s ease;
}

/* 选中状态下显示黑色线 */
.display-button.active::after, .compare-button.active::after {
    background-color: black;
}

.display-button.active, .compare-button.active {
    background-color: #F3F3F3;
}

.detail-view-title {
    width: 100%;
    height: 100%;
    /* 居中显示 */
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 17px;
    font-weight: bold;

    position: relative;
    background-color: #F3F3F3;
}

.detail-view-title::after {
    content: '';
    position: absolute;
    left: 2.5%;
    bottom: 0;
    width: 95%;
    height: 2px;
    background-color: black;
}

.control-content {
    /* 保持长宽比 313: 697 */
    /* aspect-ratio: 313 / 697; */
    width: 100%;
    height: 95.35%;
    display: flex;
    flex-direction: column;
    /* justify-content: center; */
    align-items: center;

    /* 上下边距 左右边距 */
    padding: 10px 5px;
    box-sizing: border-box;

    /* gap: 10px; */
}

.display-mode {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;

    gap: 10px;
}

.display-selection-area {
    /* 高度 49 */
    width: 100%;
    height: 3.5%;
    display: flex;
    align-items: center;
    justify-content: space-between;

    /* font-size: 13px; */
}

.display-selectionBox {
    /* 126 * 24 */
    width: 40%;
    height: 100%;

    font-size: 12px;
    border-radius: 5px;
    border: 1px solid #D0D5DD;

    margin-left: 5%;
}

.display-checkbox {
    width: 50%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.display-checkbox label {
    font-size: 12px;
    color: #000000;
}

.horizontal-divider {
    width: 95%;
    height: 2px;
    background-color: #EAEAEA;

    margin-top: -2.5px;
    margin-bottom: -2.5px;
}

.display-motion-name-area {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;

    padding-left: 5%;
    box-sizing: border-box;

    gap: 3%;
}

.display-motion-title {
    font-weight: bold;
}

.display-motion-name {

}

.display-keyattributes-area {
    width: 100%;
    /* height: 30%; */
    max-height: 500px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;

    padding-left: 5%;
    box-sizing: border-box;

    gap: 10px;

    overflow: scroll;
}

.display-keyattributes-title-area {
    width: 100%;
    display: flex;

    align-items: center;
    justify-content: flex-start;

    gap: 3%;
}

.display-keyattributes-title {
    font-weight: bold;
}

.display-keyattribute-item-area {
    width: 100%;
    /* height: 100%; */
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;

    /* gap: 5px; */
}

.display-keyattribute-item-title {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 10px;
}

.display-keyattribute-id {
    width: 13px;
    height: 13px;
    border-radius: 50%;
    border: 1px solid #000000;
    /* background-color: white; */
    /* color: black; */
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 0.8em;
}

.display-keyattribute-text {
    font-size: 0.9em;
    /* font-weight: bold; */
    color: #000000;
}

.chart-container {
    width: 100%;
    /* height: 100%; */
    position: relative;
}

.display-markFrame-area {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;

    padding-left: 5%;
    padding-right: 5%;
    box-sizing: border-box;

    gap: 10px;
}

.display-markFrame-selectionBox-area {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    
    gap: 3%;
    overflow-x: scroll;
}

.display-markFrame-selectionBox {
    min-width: 40px;
    min-height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;

    border: 3px solid #A3A3A3;
    font-weight: bold;
}

.display-markFrame-button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;

    border: 1px solid #D0D5DD;
    border-radius: 10px;

    padding: 5px 10px;
    box-sizing: border-box;
    gap: 10px;
}

.mark-icon {
    /* width: 100%; */
    /* height: 100%; */
    height: 19.5px;
    display: flex;
    align-items: center;
    justify-content: center;
    /* margin-left: 1px; */
}

.display-markFrame-button-text {
    font-size: 18px;
    font-weight: bold;
}

.compare-mode {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;

    gap: 10px;
}

.compare-selection-area {
    /* 高度 24 */
    width: 100%;
    height: 3.5%;
    display: flex;
    align-items: center;
    justify-content: space-between;

    font-size: 12px;
}

.compare-selectionBox {
    /* 126 * 24 */
    width: 40%;
    height: 100%;

    font-size: 12px;
    border-radius: 5px;
    border: 1px solid #D0D5DD;
}

.compare-comparisonBox-area {
    aspect-ratio: 217 / 460;
    width: 100%;
    /* height: 96.5%; */
    /* height: 460px; */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    gap: 10px;

    overflow-y: scroll;

    padding: 0 5px;
    box-sizing: border-box;
}

.compare-comparisonBox {
    /* 保持长宽比 286: 91 */
    aspect-ratio: 286 / 91;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #D9D9D9;
    border-radius: 5px;
}

.highlight-box {
    /* border: 3px solid #C59CF4; */
    /* background-color: #F0E6FF; */
    background-color: orange;
}

.compare-comparisonBox-title {
    width: 100%;
    height: 33%;
    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 1.2em;
    font-weight: bold;
    color: #2E4051;
}

.compare-comparisonBox-content {
    /* 高度 61 */
    width: 100%;
    height: 67%;
    display: flex;
    align-items: center;
    justify-content: space-evenly;

    position: relative;
}

.compare-comparisonBox-data {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 1.2em;
    /* font-weight: bold; */
    color: #D09837;
}

.vertical-divider {
    width: 2px;
    height: 80%;
    background-color: #000000;

    /* margin-left: 50%; */
    position: absolute;
    left: 50%;
}

.detail-view {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

/* .detail-view p {
    font-size: 0.8em;
    color: #2E4051;
    margin: 5px 0;
} */

/* .highlight {
    color: #F7877C;
} */

.Snapshot {
    /* 297 * 165 */
    width: 100%;
    height: 165px;
    display: flex;
    align-items: center;
    flex-direction: column;

    border: 1px solid #EAEAEA;
    border-radius: 5px;
    background-color: #FFFFFF;
}

.Feedback {
    /* 297 * 135 */
    width: 100%;
    height: 135px;
    display: flex;
    align-items: center;
    flex-direction: column;

    border: 1px solid #EAEAEA;
    border-radius: 5px;
    background-color: #FFFFFF;

    margin-top: 10px;
}

.Relative-Constraints {
    /* 297 * 165 */
    width: 100%;
    height: 165px;
    display: flex;
    align-items: center;
    flex-direction: column;

    border: 1px solid #EAEAEA;
    border-radius: 5px;
    background-color: #FFFFFF;

    margin-top: 10px;
}

.Visualization {
    /* 297 * 183 */
    width: 100%;
    height: 183px;
    display: flex;
    align-items: center;
    flex-direction: column;

    border: 1px solid #EAEAEA;
    border-radius: 5px;
    background-color: #FFFFFF;

    margin-top: 10px;
}

.Snapshot-title, .Feedback-title, .Relative-Constraints-title, .Visualization-title {
    width: 100%;
    height: 30px;

    display: flex;
    align-items: center;
    padding-left: 5px;
    box-sizing: border-box;

    font-size: 16px;
    font-weight: bold;
    color: #000000;
    /* margin: 5px 0; */
}

.Snapshot-content {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 12px;
    color: #000000;
}

.Snapshot-content-left {
    width: 50%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;

    gap: 8px;
    padding: 6px 5px;
    box-sizing: border-box;
}

.Snapshot-key-pose {
    width: 100%;
    height: auto;
    display: flex;
    align-items: center;
    justify-content: flex-start;

    gap: 10px;
}

.Snapshot-frame {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;

    gap: 5px;
}

.Snapshot-body-part {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;

    gap: 5px;
}

.Snapshot-key-pose-title, .Snapshot-frame-title, .Snapshot-body-part-title {
    font-size: 14px;
    font-weight: bold;
    color: #000000;
}

.Snapshot-key-pose-no {
    border: 2px solid #F3F3F3;
    border-radius: 5px;
    padding: 2px 10px;
    box-sizing: border-box;
}

.Snapshot-frame-nos {
    width: 90%;
    height: auto;
    display: flex;
    align-items: center;
    justify-content: flex-start;

    background-color: #F3F3F3;
    border-radius: 5px;
    padding: 2px;
    box-sizing: border-box;
}

.Snapshot-frame-start, .Snapshot-frame-end {
    width: 50%;
    display: flex;
    align-items: center;
    justify-content: center;

    padding-top: 1px;
    padding-bottom: 1px;
    box-sizing: border-box;
}

.Snapshot-frame-start {
    background-color: #FFFFFF;
    border-radius: 5px;
}

.Snapshot-body-part-items {
    width: 100%;
    height: auto;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 10px;
}

.Snapshot-body-part-item {
    width: 40%;
    display: flex;
    align-items: center;
    justify-content: center;

    color: #FFFFFF;
    background-color: #F7877C;
    border-radius: 5px;

    padding: 2px 5px;
    box-sizing: border-box;
}

.Snapshot-content-right {
    width: 50%;
    height: auto;
    align-items: center;
    justify-content: center;
}

.Feedback-content {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 16px;
    color: #000000;
    text-align: left;

    white-space: pre-wrap;
}

.Relative-Constraints-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;

    padding: 8px 5px;
    box-sizing: border-box;
    gap: 10px;
}

.Relative-Constraints-item {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-start;

    font-size: 16px;
}

.Relative-Constraints-item-no {
    width: 10%;
    display: flex;
    align-items: center;
    font-weight: bold;
}

.Relative-Constraints-item-type {
    width: 30%;
    display: flex;
    align-items: center;
    font-weight: bold;
}

.Relative-Constraints-item-joints {
    width: 60%;
    display: flex;
    align-items: center;
}

.Visualization-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    padding: 0 5px;
    box-sizing: border-box;
}

.Visualization-option {
    width: 100%;
    height: 25%;
    display: flex;
    align-items: center;
    /* justify-content: center; */

    gap: 5px;
}

.Visualization-option-playMenu {
    position: absolute;
    width: 100%;
    height: 25%;
    display: flex;
    align-items: center;
    justify-content: center;
    bottom: 0;
}

.Visualization-option-title {
    width: 20%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    font-size: 15px;
    font-weight: bold;
}

.Visualization-option-bar {
    width: 68%;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    background-color: #F3F3F3;
    border-radius: 5px;

    padding: 3px 3px;
    box-sizing: border-box;
}

.Visualization-option-bar div {
    flex: 1;
}

.Visualization-option-bar-item {
    /* width: auto; */
    display: flex;
    align-items: center;
    justify-content: center;

    /* background-color: #FFFFFF; */
    /* border-radius: 5px; */

    padding: 2px 5px;
    box-sizing: border-box;
    
    font-size: 14px;

    transition: background-color 0.3s ease; /* 平滑过渡效果 */
}

.Visualization-option-bar-item.active {
    background-color: #FFFFFF;
    border-radius: 5px;
}

.clip-horizontal-divider {
    width: 95%;
    height: 2px;
    background-color: #EAEAEA;

    /* margin-top: -2.5px;
    margin-bottom: -2.5px; */
}

.playMenu-container {
    position: absolute;
    width: 300px;
    height: 70px;
    left: 40%;
    top: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: transparent;
    z-index: 10;
    border: 4px solid #E8EBF0;
    border-radius: 20px;
}

.playMenu-icon {
    width: 50px;
    height: 50px;
}

.playMenu {
    position: absolute;
    width: 100%;
    height: 50px;
    top: 0;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
}

.playMenu-text {
    position: absolute;
    width: 100%;
    font-size: 1.2em;
    font-weight: 600;
    color: black;
    bottom: 0;
    background: rgba(243, 243, 243, 1.0);
}
</style>