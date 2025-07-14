<template>
    <div class="constraint-name-text">
        {{ constraintName }}
    </div>
    <div class="image-container">
        
        <img :src="imageSrc" alt="segment image" class="segment-image" @load="onImageLoad" />

        <!-- 非编辑模式下静态显示 -->
        <!-- 绘制骨架连接线、坐标轴、constraint等内容 -->
        <svg v-if="!isEditing" class="connection-lines" :width="imageWidth+2*imageOffsetX" :height="imageHeight+2*imageOffsetY">
            <!-- 灰色骨架线 -->
            <line
                v-for="(line, index) in skeletonLines"
                :key="'skeleton-' + index"
                :x1="transformX(line.x1)"
                :y1="transformY(line.y1)"
                :x2="transformX(line.x2)"
                :y2="transformY(line.y2)"
                stroke="#A3A3A3"
                stroke-width="3"
            />

            <!-- 绘制 x, y, z 轴的短直线 -->
            <line
                v-for="(line, index) in axisLines"
                :key="'axis-' + index"
                :x1="transformX(line.x1)"
                :y1="transformY(line.y1)"
                :x2="transformX(line.x2)"
                :y2="transformY(line.y2)"
                :stroke="line.color"
                stroke-width="3"
            />

            <!-- 绘制 distance 类型的连接线 -->
            <line
                v-for="(line, index) in distanceLines"
                :key="'distance-' + index"
                :x1="transformX(line.x1)"
                :y1="transformY(line.y1)"
                :x2="transformX(line.x2)"
                :y2="transformY(line.y2)"
                stroke="#F7877C"
                stroke-width="3"
            />

            <!-- 绘制 angle 类型的连接线 -->
            <line
                v-for="(line, index) in angleLines"
                :key="'angle-line-' + index"
                :x1="transformX(line.x1)"
                :y1="transformY(line.y1)"
                :x2="transformX(line.x2)"
                :y2="transformY(line.y2)"
                stroke="#F7877C"
                stroke-width="3"
            />

            <!-- 绘制夹角弧线 -->
            <path
                v-for="(arc, index) in angleArcs"
                :key="'angle-arc-' + index"
                :d="arc.d"
                stroke="#F7877C"
                stroke-width="3"
                fill="none"
            />

            <!-- 绘制 ground 水平线 -->
            <line
                v-if="groundLine"
                :x1="transformX(groundLine.x1)"
                :y1="transformY(groundLine.y1)"
                :x2="transformX(groundLine.x2)"
                :y2="transformY(groundLine.y2)"
                :stroke="groundLine.color"
                stroke-width="3"
            />
        </svg>

        <!-- 绘制关键点圆点 -->
        <div
            v-if="!isEditing"
            v-for="(point, key) in keypoints"
            :key="key"
            class="keypoint"
            :style="{
                left: `${(point.x * scaleX) + imageOffsetX}px`,
                top: `${(point.y * scaleY) + imageOffsetY}px`,
                borderColor: isJointInSelectedConstraint(key) ? '#F7877C' : '#A3A3A3',
            }"
        ></div>

        <!-- 编辑模式可进行交互 -->
        <!-- 绘制骨架连接线、坐标轴、constraint等内容 -->
        <svg v-if="isEditing" class="connection-lines" :width="imageWidth+2*imageOffsetX" :height="imageHeight+2*imageOffsetY" style="pointer-events: auto;">
            <!-- 灰色骨架线 -->
            <line
                v-for="(line, index) in skeletonLines"
                :key="'skeleton-' + index"
                :x1="transformX(line.x1)"
                :y1="transformY(line.y1)"
                :x2="transformX(line.x2)"
                :y2="transformY(line.y2)"
                stroke="#A3A3A3"
                stroke-width="3"
            />

            <!-- 绘制 ground 水平线 -->
            <line
                v-if="groundLine"
                :x1="transformX(groundLine.x1)"
                :y1="transformY(groundLine.y1)"
                :x2="transformX(groundLine.x2)"
                :y2="transformY(groundLine.y2)"
                :stroke="selectedGround ? '#F7877C' : '#A3A3A3'"
                stroke-width="3"
                @click="handleGroundClick"
            />

            <!-- 绘制选中的关键点的XYZ坐标轴短直线 -->
            <line
                v-for="(line, index) in selectedKeypointAxisLines"
                :key="'axis-' + index"
                :x1="transformX(line.x1)"
                :y1="transformY(line.y1)"
                :x2="transformX(line.x2)"
                :y2="transformY(line.y2)"
                :stroke="line.color"
                stroke-width="3"
                @click="handleAxisClick(line.keypoint, line.axis)"
            />

            <!-- 绘制关键点之间的连线 -->
            <line
                v-for="(line, index) in linesBetweenKeypoints"
                :key="'line-' + index"
                :x1="transformX(line.x1)"
                :y1="transformY(line.y1)"
                :x2="transformX(line.x2)"
                :y2="transformY(line.y2)"
                :stroke="line.isSolid ? '#F7877C' : '#A3A3A3'"
                :stroke-dasharray="line.isSolid ? 'none' : '5,5'"
                stroke-width="3"
            />

            <!-- 绘制夹角弧线 -->
            <path
                v-for="(arc, index) in editingAngleArcs"
                :key="'editing-angle-arc-' + index"
                :d="arc.d"
                :stroke="arc.color"
                stroke-width="3"
                fill="none"
            />
        </svg>
        
        <!-- 绘制关键点圆点 -->
        <div
            v-if="isEditing"
            v-for="(point, key) in keypoints"
            :key="key"
            class="keypoint"
            :style="{
                left: `${(point.x * scaleX) + imageOffsetX}px`,
                top: `${(point.y * scaleY) + imageOffsetY}px`,
                borderColor: selectedKeypoints.includes(key) ? '#F7877C' : '#A3A3A3',
            }"
            @click="handleKeypointClick(key)"
        ></div>

        <!-- 右上角的矩形 -->
        <div class="constraint-rectangles">
            <div
                v-for="constraint in constraints"
                :key="constraint.id"
                class="constraint-rectangle"
                :class="{ active: selectedConstraint === constraint.id }"
                @click="handleConstraintClick(constraint)"
            >
                C. {{ constraint.id }}
            </div>

            <!-- 新增的 "+" 矩形选项框 -->
            <div
                class="constraint-rectangle"
                :class="{ active: isEditing }"
                @click="handleAddConstraintClick"
            >
                +
            </div>
        </div>
        <!-- <div
            v-for="(point, key) in keypoints"
            :key="key"
            class="keypoint"
            :style="{
                left: `${Point.x * scaleX}px`,
                top: `${Point.y * scaleY}px`,
            }"
        ></div> -->
    </div>
</template>

<script>
export default {
    name: 'ImageWithKeypoints',
    props: {
        imageSrc: {
            type: String,
            required: true,
        },
        constraints: {
            type: Array,
            default: () => [],
        },
        keypoints: {
            type: Object,
            default: () => ({}),
        },
    },
    data() {
        return {
            scaleX: 1,
            scaleY: 1,
            imageWidth: 0,
            imageHeight: 0,
            imageOffsetX: 0, // 图片的水平偏移量
            imageOffsetY: 0, // 图片的垂直偏移量
            selectedConstraint: null, // 当前选中的 constraint id
            isEditing: false,       // 是否处于编辑模式
            selectedKeypoints: [], // 当前选中的关键点名称数组
            // selectedAxes: [],      // 当前选中的坐标轴数组
            selectedAxes: {},      // 记录每个关键点的选中坐标轴，格式为 { keypointName: ['x', 'y', 'z'] }
            linesBetweenKeypoints: [], // 存储关键点之间的连线
            selectedGround: false, // 是否选中了 ground 直线
            // angleArcs: [], // 存储夹角弧线 angleArcs 属性与计算属性中的 angleArcs 重名会导致冲突
            editingAngleArcs: [], // 存储编辑模式下的夹角弧线
        };
    },
    computed: {
        // 计算constraint的名称字符串
        constraintName() {
            if (this.selectedConstraint === null) return '';
            const constraint = this.constraints.find(
                constraint => constraint.id === this.selectedConstraint
            );
            // return constraint ? constraint.type + ": " : '';
            if (!constraint) return '';
            

            // 从约束条件中提取所有关节名称
            // const jointNames = constraint.joints.map(jointObj => {
            //     // 获取关节对象中的第一个键（joint_1, joint_2等）
            //     const jointKey = Object.keys(jointObj)[0];
            //     return jointObj[jointKey].name; // 返回关节名称
            // });

            // 首字母大写
            // 1. 处理约束类型：首字母大写（如 "angle" → "Angle"）
            const capitalizedType = constraint.type.charAt(0).toUpperCase() + constraint.type.slice(1);

            // 2. 处理关节名称：每个单词首字母大写（如 "left_ankle" → "Left_Ankle"）
            const jointNames = constraint.joints.map(jointObj => {
                const jointKey = Object.keys(jointObj)[0];

                // const displayName = jointObj[jointKey].name
                //     .replace(/^left_/i, 'L_')  // 开头的 "left_" → "L_"
                //     .replace(/^right_/i, 'R_') // 开头的 "right_" → "R_"
                //     .split('_') // 拆分下划线连接的单词（如 ["left", "ankle"]）
                //     .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // 每个单词首字母大写
                //     .join('_'); // 重新拼接（保持原有下划线）

                return jointObj[jointKey].name
                    .replace(/^left_/i, 'L_')  // 开头的 "left_" → "L_"
                    .replace(/^right_/i, 'R_') // 开头的 "right_" → "R_"
                    .split('_') // 拆分下划线连接的单词（如 ["left", "ankle"]）
                    .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // 每个单词首字母大写
                    .join('_'); // 重新拼接（保持原有下划线）
            });
            
            // 返回格式: "类型: 关节1~关节2~关节3..."
            return `${capitalizedType}: ${jointNames.join('~')}`;
        },

        // 定义骨架连接线
        skeletonLines() {
            // const lines = [];
            const connections = [
                ['head', 'neck'], // 头部到颈部
                ['neck', 'right_elbow'], // 颈部到右肘
                ['right_elbow', 'right_wrist'], // 右肘到右腕
                ['neck', 'left_elbow'], // 颈部到左肘
                ['left_elbow', 'left_wrist'], // 左肘到左腕
                ['neck', 'hip'], // 颈部到臀部
                ['hip', 'right_knee'], // 臀部到右膝
                ['right_knee', 'right_ankle'], // 右膝到右踝
                ['hip', 'left_knee'], // 臀部到左膝
                ['left_knee', 'left_ankle'], // 左膝到左踝
            ];

            // connections.forEach(([joint1, joint2]) => {
            //     if (this.keypoints[joint1] && this.keypoints[joint2]) {
            //         lines.push({
            //             x1: this.keypoints[joint1].x,
            //             y1: this.keypoints[joint1].y,
            //             x2: this.keypoints[joint2].x,
            //             y2: this.keypoints[joint2].y,
            //         });
            //     }
            // });

            // return lines;

            return connections.reduce((lines, [j1, j2]) => {
                if (this.keypoints[j1] && this.keypoints[j2]) {
                    lines.push({
                        x1: this.keypoints[j1].x,
                        y1: this.keypoints[j1].y,
                        x2: this.keypoints[j2].x,
                        y2: this.keypoints[j2].y
                    });
                }
                return lines;
            }, []);

        },

        // 定义 x, y, z 轴的短直线
        axisLines() {
            const lines = [];
            const axisLength = 50 * Math.min(this.scaleX, this.scaleY); // 轴线的长度

            // 如果没有选中的 constraint，返回空数组
            if (this.selectedConstraint === null) return lines;

            // 找到当前选中的 constraint
            const selectedConstraint = this.constraints.find(
                constraint => constraint.id === this.selectedConstraint
            );

            if (!selectedConstraint) return lines;

            if (selectedConstraint.type === 'trajectory') {
                // 遍历 constraint 中的 joints
                selectedConstraint.joints.forEach(joint => {
                    const jointKey = Object.keys(joint)[0]; // 获取 joint 的 key
                    const jointData = joint[jointKey]; // 获取 joint 的数据
                    const jointName = jointData.name; // 获取 joint 的名称
                    const property = jointData.property; // 获取 property

                    const point = this.keypoints[jointName];

                    lines.push({
                        x1: point.x,
                        y1: point.y,
                        x2: point.x + axisLength,
                        y2: point.y,
                        color: '#F7877C',
                    });

                    lines.push({
                        x1: point.x,
                        y1: point.y,
                        x2: point.x - axisLength / 1.414,
                        y2: point.y + axisLength / 1.414,
                        color: '#F7877C',
                    });

                    lines.push({
                        x1: point.x,
                        y1: point.y,
                        x2: point.x,
                        y2: point.y - axisLength,
                        color: '#F7877C',
                    });
                })

                return lines;
            }

            // 遍历 constraint 中的 joints
            selectedConstraint.joints.forEach(joint => {
                const jointKey = Object.keys(joint)[0]; // 获取 joint 的 key，如 joint_1, joint_2
                const jointData = joint[jointKey]; // 获取 joint 的数据
                const jointName = jointData.name; // 获取 joint 的名称，如 head, neck
                const property = jointData.property; // 获取 property，如 x, y, z

                // console.log('Joint:', joint);
                // console.log('Joint key:', jointKey);
                // console.log('Joint data:', jointData);
                // console.log('Joint name:', jointName);
                // console.log('Property:', property);

                // 如果 property 是 x, y, z 之一，并且关键点存在
                if (['x', 'y', 'z'].includes(property) && this.keypoints[jointName]) {
                    const point = this.keypoints[jointName];

                    console.log('Point:', point);

                    lines.push({
                        x1: point.x,
                        y1: point.y,
                        x2: point.x + axisLength,
                        y2: point.y,
                        color: property === 'x' ? '#F7877C' : '#A3A3A3',
                    });

                    lines.push({
                        x1: point.x,
                        y1: point.y,
                        x2: point.x - axisLength / 1.414,
                        y2: point.y + axisLength / 1.414,
                        color: property === 'y' ? '#F7877C' : '#A3A3A3',
                    });

                    lines.push({
                        x1: point.x,
                        y1: point.y,
                        x2: point.x,
                        y2: point.y - axisLength,
                        color: property === 'z' ? '#F7877C' : '#A3A3A3',
                    });

                    // 根据 property 绘制对应的轴线
                    // if (property === 'x') {
                    //     lines.push({
                    //         x1: point.x,
                    //         y1: point.y,
                    //         x2: point.x + axisLength,
                    //         y2: point.y,
                    //     });
                    // } else if (property === 'y') {
                    //     lines.push({
                    //         x1: point.x,
                    //         y1: point.y,
                    //         x2: point.x,
                    //         y2: point.y + axisLength,
                    //     });
                    // } else if (property === 'z') {
                    //     lines.push({
                    //         x1: point.x,
                    //         y1: point.y,
                    //         x2: point.x + axisLength,
                    //         y2: point.y + axisLength,
                    //     });
                    // }
                }
            });

            // Object.keys(this.keypoints).forEach(key => {
            //     const point = this.keypoints[key];
            //     if (point.x !== undefined) {
            //         // 绘制 x 轴
            //         lines.push({
            //             x1: point.x,
            //             y1: point.y,
            //             x2: point.x + axisLength,
            //             y2: point.y,
            //         });
            //     }
            //     if (point.y !== undefined) {
            //         // 绘制 y 轴
            //         lines.push({
            //             x1: point.x,
            //             y1: point.y,
            //             x2: point.x,
            //             y2: point.y + axisLength,
            //         });
            //     }
            //     if (point.z !== undefined) {
            //         // 绘制 z 轴（假设 z 轴垂直于屏幕）
            //         lines.push({
            //             x1: point.x,
            //             y1: point.y,
            //             x2: point.x + axisLength,
            //             y2: point.y + axisLength,
            //         });
            //     }
            // });

            // 如果 constraint 的 type 是 distance，绘制连接线
            // if (selectedConstraint.type === 'distance') {
            //     const joints = selectedConstraint.joints;
            //     if (joints.length >= 2) {
            //         const joint1 = joints[0][Object.keys(joints[0])[0]]; // 获取第一个 joint
            //         const joint2 = joints[1][Object.keys(joints[1])[0]]; // 获取第二个 joint

            //         const point1 = this.keypoints[joint1.name];
            //         const point2 = this.keypoints[joint2.name];

            //         if (point1 && point2) {
            //             lines.push({
            //                 x1: point1.x,
            //                 y1: point1.y,
            //                 x2: point2.x,
            //                 y2: point2.y,
            //                 color: '#F7877C', // distance 连接线颜色
            //             });
            //         }
            //     }
            // }
            
            console.log('Axis lines:', lines);
            return lines;
        },

        // 定义 distance 类型的连接线
        distanceLines() {
            const lines = [];

            // 如果没有选中的 constraint，返回空数组
            if (this.selectedConstraint === null) return lines;

            // 找到当前选中的 constraint
            const selectedConstraint = this.constraints.find(
                constraint => constraint.id === this.selectedConstraint
            );

            if (!selectedConstraint || selectedConstraint.type !== 'distance') return lines;

            // 获取 distance 类型的 constraint 的 joints
            const joints = selectedConstraint.joints;
            if (joints.length >= 2) {
                const joint1 = joints[0][Object.keys(joints[0])[0]]; // 获取第一个 joint
                const joint2 = joints[1][Object.keys(joints[1])[0]]; // 获取第二个 joint

                const point1 = this.keypoints[joint1.name];
                const point2 = this.keypoints[joint2.name];

                // if (point1 && point2) {
                //     lines.push({
                //         x1: point1.x,
                //         y1: point1.y,
                //         x2: point2.x,
                //         y2: point2.y,
                //     });
                // }

                // 检查是否有一个节点是 ground
                const isJoint1Ground = joint1.name === 'ground';
                const isJoint2Ground = joint2.name === 'ground';

                if (isJoint1Ground || isJoint2Ground) {
                    // 如果有一个节点是 ground，则从另一个节点绘制一条竖直线到 ground
                    const node = isJoint1Ground ? point2 : point1;
                    const groundY = this.groundLine ? this.groundLine.y1 : null;

                    if (node && groundY !== null) {
                        lines.push({
                            x1: node.x,
                            y1: node.y,
                            x2: node.x,
                            y2: groundY,
                            // color: '#F7877C',
                        });

                        // 将 ground 直线的颜色也设置为 #F7877C
                        // lines.push({
                        //     x1: 0, // 从最左侧开始
                        //     y1: groundY,
                        //     x2: this.imageWidth / this.scaleX, // 到最右侧结束
                        //     y2: groundY,
                        //     color: '#F7877C',
                        // });
                    }
                } else if (point1 && point2) {
                    // 如果两个节点都不是 ground，则绘制它们之间的连线
                    lines.push({
                        x1: point1.x,
                        y1: point1.y,
                        x2: point2.x,
                        y2: point2.y,
                        // color: '#F7877C',
                    });
                }
            }

            return lines;
        },

        // 定义 angle 类型的连接线
        angleLines() {
            const lines = [];

            // 如果没有选中的 constraint，返回空数组
            if (this.selectedConstraint === null) return lines;

            // 找到当前选中的 constraint
            const selectedConstraint = this.constraints.find(
                constraint => constraint.id === this.selectedConstraint
            );

            if (!selectedConstraint || selectedConstraint.type !== 'angle') return lines;

            // 检查是否所有节点的 property 均为 'a'
            // const joints = selectedConstraint.joints;
            // if (joints.length === 3 && joints.every(joint => {
            //     const jointKey = Object.keys(joint)[0];
            //     return joint[jointKey].property === 'a';
            // })) {
            //     const joint1 = joints[0][Object.keys(joints[0])[0]];
            //     const joint2 = joints[1][Object.keys(joints[1])[0]];
            //     const joint3 = joints[2][Object.keys(joints[2])[0]];

            //     const point1 = this.keypoints[joint1.name];
            //     const point2 = this.keypoints[joint2.name];
            //     const point3 = this.keypoints[joint3.name];

            //     if (point1 && point2 && point3) {
            //         // 绘制节点一和节点二之间的连线
            //         lines.push({
            //             x1: point1.x,
            //             y1: point1.y,
            //             x2: point2.x,
            //             y2: point2.y,
            //         });

            //         // 绘制节点二和节点三之间的连线
            //         lines.push({
            //             x1: point2.x,
            //             y1: point2.y,
            //             x2: point3.x,
            //             y2: point3.y,
            //         });
            //     }
            // }

            // 获取所有节点
            const joints = selectedConstraint.joints;
            if (joints.length === 3) {
                const joint1 = joints[0][Object.keys(joints[0])[0]];
                const joint2 = joints[1][Object.keys(joints[1])[0]];
                const joint3 = joints[2][Object.keys(joints[2])[0]];

                const point1 = this.keypoints[joint1.name];
                const point2 = this.keypoints[joint2.name];
                const point3 = this.keypoints[joint3.name];

                if (point1 && point2 && point3) {
                    // 检查 property 是否为 'a'
                    const isJoint1A = joint1.property === 'a';
                    const isJoint2A = joint2.property === 'a';
                    const isJoint3A = joint3.property === 'a';

                    // 如果两个节点的 property 为 'a'，则绘制它们之间的连线
                    if (isJoint1A && isJoint2A) {
                        lines.push({
                            x1: point1.x,
                            y1: point1.y,
                            x2: point2.x,
                            y2: point2.y,
                        });
                    }
                    if (isJoint2A && isJoint3A) {
                        lines.push({
                            x1: point2.x,
                            y1: point2.y,
                            x2: point3.x,
                            y2: point3.y,
                        });
                    }
                }
            }

            return lines;
        },

        // 定义夹角弧线
        angleArcs() {
            const arcs = [];

            // 如果没有选中的 constraint，返回空数组
            if (this.selectedConstraint === null) return arcs;

            // 找到当前选中的 constraint
            const selectedConstraint = this.constraints.find(
                constraint => constraint.id === this.selectedConstraint
            );

            if (!selectedConstraint || selectedConstraint.type !== 'angle') return arcs;

            // 检查是否所有节点的 property 均为 'a'
            // const joints = selectedConstraint.joints;
            // if (joints.length === 3 && joints.every(joint => {
            //     const jointKey = Object.keys(joint)[0];
            //     return joint[jointKey].property === 'a';
            // })) {
            //     const joint1 = joints[0][Object.keys(joints[0])[0]];
            //     const joint2 = joints[1][Object.keys(joints[1])[0]];
            //     const joint3 = joints[2][Object.keys(joints[2])[0]];

            //     const point1 = this.keypoints[joint1.name];
            //     const point2 = this.keypoints[joint2.name];
            //     const point3 = this.keypoints[joint3.name];

            //     console.log(joint1.name, joint2.name, joint3.name);

            //     if (point1 && point2 && point3) {
            //         // 对关键点坐标进行缩放换算
            //         const scaledPoint1 = {
            //             // x: point1.x * this.scaleX + this.imageOffsetX,
            //             // y: point1.y * this.scaleY + this.imageOffsetY,
            //             x: this.transformX(point1.x),
            //             y: this.transformY(point1.y),
            //         };
            //         const scaledPoint2 = {
            //             // x: point2.x * this.scaleX + this.imageOffsetX,
            //             // y: point2.y * this.scaleY + this.imageOffsetY,
            //             x: this.transformX(point2.x),
            //             y: this.transformY(point2.y),
            //         };
            //         const scaledPoint3 = {
            //             // x: point3.x * this.scaleX + this.imageOffsetX,
            //             // y: point3.y * this.scaleY + this.imageOffsetY,
            //             x: this.transformX(point3.x),
            //             y: this.transformY(point3.y),
            //         };

            //         // 计算夹角弧线的路径
            //         const radius = 20; // 弧线半径
            //         // const angle = this.calculateAngle(point1, point2, point3);
            //         // const startAngle = this.calculateAngleBetweenPoints(point2, point1);
            //         // const endAngle = this.calculateAngleBetweenPoints(point2, point3);
            //         const angle = this.calculateAngle(scaledPoint1, scaledPoint2, scaledPoint3);
            //         const startAngle = this.calculateAngleBetweenPoints(scaledPoint2, scaledPoint1);
            //         const endAngle = this.calculateAngleBetweenPoints(scaledPoint2, scaledPoint3);

            //         console.log('Angle:', angle);
            //         console.log('Start angle:', startAngle);
            //         console.log('End angle:', endAngle);

            //         // 绘制弧线
            //         arcs.push({
            //             // d: this.describeArc(point2.x, point2.y, radius, startAngle, endAngle),
            //             d: this.describeArc(scaledPoint2.x, scaledPoint2.y, radius, startAngle, endAngle),
            //         });
            //     }
            // }

            // 获取所有节点
            const joints = selectedConstraint.joints;
            if (joints.length === 3) {
                const joint1 = joints[0][Object.keys(joints[0])[0]];
                const joint2 = joints[1][Object.keys(joints[1])[0]];
                const joint3 = joints[2][Object.keys(joints[2])[0]];

                const point1 = this.keypoints[joint1.name];
                const point2 = this.keypoints[joint2.name];
                const point3 = this.keypoints[joint3.name];

                if (point1 && point2 && point3) {
                    // 对关键点坐标进行缩放换算
                    const scaledPoint1 = {
                        x: this.transformX(point1.x),
                        y: this.transformY(point1.y),
                    };
                    const scaledPoint2 = {
                        x: this.transformX(point2.x),
                        y: this.transformY(point2.y),
                    };
                    const scaledPoint3 = {
                        x: this.transformX(point3.x),
                        y: this.transformY(point3.y),
                    };

                    // 检查 property 是否为 'a'
                    const isJoint1A = joint1.property === 'a';
                    // const isJoint2A = joint2.property === 'a';
                    const isJoint3A = joint3.property === 'a';

                    // 确定夹角边
                    let startPoint, endPoint;

                    // 如果节点一的 property 为 'a'，则以节点一和节点二的连线为夹角边
                    if (isJoint1A) {
                        startPoint = scaledPoint1;
                    } else if (['x', 'y', 'z'].includes(joint1.property)) {
                        // 如果节点一的 property 为 'x', 'y', 或 'z'，则以绘制的轴为夹角边
                        startPoint = {
                            x: scaledPoint1.x + (joint1.property === 'x' ? 30 : joint1.property === 'y' ? -30 : 0),
                            y: scaledPoint1.y + (joint1.property === 'z' ? -30 : joint1.property === 'y' ? 30 : 0),
                        };
                    }

                    // 如果节点三的 property 为 'a'，则以节点三和节点二的连线为夹角边
                    if (isJoint3A) {
                        endPoint = scaledPoint3;
                    } else if (['x', 'y', 'z'].includes(joint3.property)) {
                        // 如果节点三的 property 为 'x', 'y', 或 'z'，则以绘制的轴为夹角边
                        endPoint = {
                            x: scaledPoint3.x + (joint3.property === 'x' ? 30 : joint3.property === 'y' ? -30 : 0),
                            y: scaledPoint3.y + (joint3.property === 'z' ? -30 : joint3.property === 'y' ? 30 : 0),
                        };
                    }

                    // 如果确定了夹角边，则绘制弧线
                    if (startPoint && endPoint) {
                        const radius = 20; // 弧线半径
                        const startAngle = this.calculateAngleBetweenPoints(scaledPoint2, startPoint);
                        const endAngle = this.calculateAngleBetweenPoints(scaledPoint2, endPoint);

                        // console.log('Start angle:', startAngle);
                        // console.log('End angle:', endAngle);

                        arcs.push({
                            d: this.describeArc(scaledPoint2.x, scaledPoint2.y, radius, startAngle, endAngle),
                        });
                    }
                }
            }

            console.log('Angle arcs:', arcs);
            return arcs;
        },

        // 定义 ground 水平线
        groundLine() {
            const leftAnkle = this.keypoints.left_ankle;
            const rightAnkle = this.keypoints.right_ankle;

            if (leftAnkle && rightAnkle) {
                // 计算 left_ankle 和 right_ankle 的中点
                // const midX = (leftAnkle.x + rightAnkle.x) / 2;
                const midY = (leftAnkle.y + rightAnkle.y) / 2;

                // 向下偏移一定距离（例如 50 像素）
                const offsetY = 20;
                const groundY = midY + offsetY;
                // const groundY = this.transformY(midY + offsetY);

                // 绘制水平线，宽度为图像宽度
                // return {
                //     x1: 0, // 从最左侧开始
                //     y1: groundY, // 到 groundY 位置
                //     x2: this.imageWidth / this.scaleX, // 到最右侧结束
                //     y2: groundY, // 到 groundY 位置
                // };

                // 检查当前选中的 constraint 是否包含 ground 节点
                const selectedConstraint = this.constraints.find(
                    constraint => constraint.id === this.selectedConstraint
                );

                const isGroundInConstraint = selectedConstraint && selectedConstraint.type === 'distance' &&
                    selectedConstraint.joints.some(joint => {
                        const jointKey = Object.keys(joint)[0];
                        return joint[jointKey].name === 'ground';
                    });

                // 设置 ground 直线的颜色
                const color = isGroundInConstraint ? '#F7877C' : '#A3A3A3';

                // 返回 ground 直线的坐标和颜色
                return {
                    x1: this.imageWidth / this.scaleX * 0.15, // 从最左侧开始
                    y1: groundY,
                    x2: this.imageWidth / this.scaleX * 0.9, // 到最右侧结束
                    y2: groundY,
                    color: color,
                };
            }

            return null;
        },

        // 定义选中的关键点的XYZ坐标轴短直线
        selectedKeypointAxisLines() {
            const lines = [];
            const axisLength = 50 * Math.min(this.scaleX, this.scaleY); // 轴线的长度

            // 如果选择了三个关键点，则不绘制坐标轴
            if (this.selectedKeypoints.length >= 3) return lines;

            // 遍历选中的关键点
            this.selectedKeypoints.forEach(key => {
                const point = this.keypoints[key];
                if (point) {

                    // 获取当前关键点的选中坐标轴
                    const selectedAxes = this.selectedAxes[key] || [];

                    // 绘制X轴
                    lines.push({
                        x1: point.x,
                        y1: point.y,
                        x2: point.x + axisLength,
                        y2: point.y,
                        // color: '#F7877C', // X轴颜色
                        color: selectedAxes.includes('x') ? '#F7877C' : '#A3A3A3', // 动态设置颜色
                        axis: 'x', // 标识坐标轴类型
                        keypoint: key, // 标识所属关键点
                    });

                    // 绘制Y轴
                    lines.push({
                        x1: point.x,
                        y1: point.y,
                        x2: point.x - axisLength / 1.414,
                        y2: point.y + axisLength / 1.414,
                        // color: '#F7877C', // Y轴颜色
                        color: selectedAxes.includes('y') ? '#F7877C' : '#A3A3A3', // 动态设置颜色
                        axis: 'y', // 标识坐标轴类型
                        keypoint: key, // 标识所属关键点
                    });

                    // 绘制Z轴
                    lines.push({
                        x1: point.x,
                        y1: point.y,
                        x2: point.x,
                        y2: point.y - axisLength,
                        // color: '#F7877C', // Z轴颜色
                        color: selectedAxes.includes('z') ? '#F7877C' : '#A3A3A3', // 动态设置颜色
                        axis: 'z', // 标识坐标轴类型
                        keypoint: key, // 标识所属关键点
                    });
                }
            });

            return lines;
        },
    },
    mounted() {
        console.log('Constraints:', this.constraints); // 打印 constraints
        console.log('Keypoints:', this.keypoints); // 打印 keypoints
        // 默认选中第一个 constraint
        if (this.constraints.length > 0) {
            this.selectedConstraint = this.constraints[0].id;
        }
        else {
            this.selectedConstraint = null;
        }
        // this.$nextTick(() => {
        //     this.$refs.image.addEventListener('load', this.onImageLoad);
        // });
    },
    beforeDestroy() {
        // this.$refs.image.removeEventListener('load', this.onImageLoad);
    },
    methods: {
        // 坐标转换
        transformX(x) {
            return x * this.scaleX + this.imageOffsetX;
        },
        transformY(y) {
            return y * this.scaleY + this.imageOffsetY;
        },


        onImageLoad(event) {
            const image = event.target;
            // const container = image.parentElement;
            // this.scaleX = container.clientWidth / image.naturalWidth;
            // this.scaleY = container.clientHeight / image.naturalHeight;
            const naturalWidth = image.naturalWidth;
            const naturalHeight = image.naturalHeight;
            const displayWidth = image.clientWidth;
            const displayHeight = image.clientHeight;

            // 计算缩放比例
            this.scaleX = displayWidth / naturalWidth;
            this.scaleY = displayHeight / naturalHeight;
            console.log(this.scaleX, this.scaleY);
            console.log(naturalWidth, naturalHeight, displayWidth, displayHeight);

            // 计算图片的水平偏移量
            const containerWidth = image.parentElement.clientWidth;
            this.imageOffsetX = (containerWidth - displayWidth) / 2;

            // 计算图片的垂直偏移量
            const containerHeight = image.parentElement.clientHeight;
            this.imageOffsetY = (containerHeight - displayHeight) / 2;

            this.imageWidth = displayWidth;
            this.imageHeight = displayHeight;
        },

        // 处理 constraint 点击事件
        handleConstraintClick(constraint) {
            console.log('Clicked constraint:', constraint);
            this.selectedConstraint = constraint.id; // 更新选中的 constraint
            this.isEditing = false;
            
            // if (!this.isEditing) {
            //     console.log('Clicked constraint:', constraint);
            //     this.selectedConstraint = constraint.id; // 更新选中的 constraint
            // }
        },
        
        // 判断某个关节是否在当前选中的 constraint 中
        isJointInSelectedConstraint(jointName) {
            if (this.selectedConstraint === null) return false;

            // 找到当前选中的 constraint
            const selectedConstraint = this.constraints.find(
                constraint => constraint.id === this.selectedConstraint
            );

            if (!selectedConstraint) return false;

            // 遍历 constraint 中的 joints，检查是否包含指定的 jointName
            return selectedConstraint.joints.some(joint => {
                const jointKey = Object.keys(joint)[0]; // 获取 joint 的 key，如 joint_1, joint_2
                const jointData = joint[jointKey]; // 获取 joint 的数据
                return jointData.name === jointName; // 检查 joint 名称是否匹配
            });
        },

        // 计算三个点之间的夹角
        calculateAngle(p1, p2, p3) {
            const v1 = { x: p1.x - p2.x, y: p1.y - p2.y };
            const v2 = { x: p3.x - p2.x, y: p3.y - p2.y };
            const dot = v1.x * v2.x + v1.y * v2.y;
            const det = v1.x * v2.y - v1.y * v2.x;
            // console.log('夹角（弧度）:', Math.atan2(det, dot));
            return Math.atan2(det, dot);
        },

        // 计算两点之间的角度
        calculateAngleBetweenPoints(p1, p2) {
            return Math.atan2(p2.y - p1.y, p2.x - p1.x);
        },

        // 描述弧线路径
        describeArc(x, y, radius, startAngle, endAngle) {
            const start = this.polarToCartesian(x, y, radius, endAngle);
            const end = this.polarToCartesian(x, y, radius, startAngle);
            console.log('Start:', start);
            console.log('End:', end);

            // 计算弧线的方向（顺时针或逆时针）
            let endAngleSweep = endAngle;
            let startAngleSweep = startAngle;
            if (endAngleSweep < 0) {
                endAngleSweep += Math.PI * 2;
            }
            if (startAngleSweep < 0) {
                startAngleSweep += Math.PI * 2;
            }
            console.log('Start angle sweep:', startAngleSweep);
            console.log('End angle sweep:', endAngleSweep);
            const sweepFlag = 
                ((endAngleSweep > startAngleSweep && endAngleSweep - startAngleSweep > Math.PI) 
                || (endAngleSweep < startAngleSweep && startAngleSweep - endAngleSweep < Math.PI)) ? 1 : 0;
            // 0 顺时针 1 逆时针

            // const largeArcFlag = endAngle - startAngle <= Math.PI ? '0' : '1';
            const largeArcFlag = '0'; // 始终使用小弧线
            // const path = `M ${start.x} ${start.y} A ${radius} ${radius} 0 ${largeArcFlag} 0 ${end.x} ${end.y}`;
            // const path = `M ${start.x} ${start.y} A ${radius} ${radius} 0 ${largeArcFlag} ${sweepFlag} ${end.x} ${end.y}`;
            // console.log('弧线路径:', path);
            return `M ${start.x} ${start.y} A ${radius} ${radius} 0 ${largeArcFlag} ${sweepFlag} ${end.x} ${end.y}`;
        },

        // 极坐标转笛卡尔坐标
        polarToCartesian(centerX, centerY, radius, angle) {
            return {
                x: centerX + radius * Math.cos(angle),
                y: centerY + radius * Math.sin(angle),
            };
        },

        // 处理点击“+”按钮的事件
        handleAddConstraintClick() {
            this.isEditing = true; // 进入编辑模式
            this.selectedConstraint = null; // 清空选中的 constraint
        },

        // 处理关键点点击事件
        handleKeypointClick(key) {
            if (this.isEditing) {
                console.log('Keypoint clicked:', key);
                
                // 如果已经选中了该关键点，则取消选中
                if (this.selectedKeypoints.includes(key)) {
                    this.selectedKeypoints = this.selectedKeypoints.filter(k => k !== key);
                    // 移除该关键点的选中坐标轴记录
                    delete this.selectedAxes[key];

                    // 移除与该关键点相连的连线
                    // this.linesBetweenKeypoints = this.linesBetweenKeypoints.filter(line => {
                    //     const point1Key = Object.keys(this.keypoints).find(k => this.keypoints[k].x === line.x1 && this.keypoints[k].y === line.y1);
                    //     const point2Key = Object.keys(this.keypoints).find(k => this.keypoints[k].x === line.x2 && this.keypoints[k].y === line.y2);
                    //     return point1Key !== key && point2Key !== key; // 保留不与该关键点相连的连线
                    // });
                    this.linesBetweenKeypoints = this.linesBetweenKeypoints.filter(line => {
                        return line.key1 !== key && line.key2 !== key; // 保留不与该关键点相连的连线
                    });

                    // 移除与该关键点相关的夹角弧线
                    this.editingAngleArcs = this.editingAngleArcs.filter(arc => {
                        return !arc.keypoints || !arc.keypoints.includes(key);
                    });
                } else {
                    // 否则，将该关键点添加到选中列表中
                    this.selectedKeypoints.push(key);
                    this.selectedAxes[key] = []; // 直接为对象添加新属性
                }

                // 如果选中了两个关键点，绘制一条虚线（修改成实线）
                if (this.selectedKeypoints.length === 2) {
                    const [key1, key2] = this.selectedKeypoints;
                    const point1 = this.keypoints[key1];
                    const point2 = this.keypoints[key2];

                    if (point1 && point2) {
                        // 添加一条虚线（修改成实线）
                        this.linesBetweenKeypoints.push({
                            key1: key1,
                            key2: key2,
                            x1: point1.x,
                            y1: point1.y,
                            x2: point2.x,
                            y2: point2.y,
                            // isSolid: false, // 初始为虚线
                            isSolid: true, // 绘制实线
                            // color: '#A3A3A3', // 初始颜色
                        });
                    }
                }

                // 如果选中了一个关键点并且选中了 ground 直线，则绘制一条竖直线
                if (this.selectedKeypoints.length === 1 && this.selectedGround) {
                    const key1 = this.selectedKeypoints[0];
                    const point1 = this.keypoints[key1];
                    const groundY = this.groundLine ? this.groundLine.y1 : null;

                    if (point1 && groundY !== null) {
                        // 添加一条从关键点到 ground 的竖直线
                        this.linesBetweenKeypoints.push({
                            key1: key1,
                            key2: 'ground',
                            x1: point1.x,
                            y1: point1.y,
                            x2: point1.x,
                            y2: groundY,
                            isSolid: false, // 初始为虚线
                            color: '#A3A3A3', // 颜色为 #A3A3A3
                        });
                    }
                }

                // 如果选中了三个关键点，绘制夹角弧线
                if (this.selectedKeypoints.length === 3) {
                    const [key1, key2, key3] = this.selectedKeypoints;
                    const point1 = this.keypoints[key1];
                    const point2 = this.keypoints[key2];
                    const point3 = this.keypoints[key3];

                    if (point1 && point2 && point3) {
                        // 绘制另一条边
                        this.linesBetweenKeypoints.push({
                            key1: key3,
                            key2: key2,
                            x1: point3.x,
                            y1: point3.y,
                            x2: point2.x,
                            y2: point2.y,
                            isSolid: true, // 绘制实线
                            // color: '#A3A3A3', // 初始颜色
                        });

                        // 对关键点坐标进行缩放换算
                        const scaledPoint1 = {
                            x: this.transformX(point1.x),
                            y: this.transformY(point1.y),
                        };
                        const scaledPoint2 = {
                            x: this.transformX(point2.x),
                            y: this.transformY(point2.y),
                        };
                        const scaledPoint3 = {
                            x: this.transformX(point3.x),
                            y: this.transformY(point3.y),
                        };

                        // 计算夹角弧线的路径
                        const radius = 20; // 弧线半径
                        const startAngle = this.calculateAngleBetweenPoints(scaledPoint2, scaledPoint1);
                        const endAngle = this.calculateAngleBetweenPoints(scaledPoint2, scaledPoint3);

                        console.log('Start angle:', startAngle);
                        console.log('End angle:', endAngle);

                        // 绘制弧线
                        this.editingAngleArcs.push({
                            d: this.describeArc(scaledPoint2.x, scaledPoint2.y, radius, startAngle, endAngle),
                            color: '#F7877C', // 弧线颜色
                            keypoints: [key1, key2, key3], // 记录关联的关键点
                        });
                    }

                    // console.log('Angle arcs:', this.editingAngleArcs);
                }
            }
        },

        // 处理坐标轴点击事件
        handleAxisClick(key, axis) {
            if (this.isEditing) {
                console.log('Axis clicked:', key);

                // 获取当前关键点的选中坐标轴列表
                const axes = this.selectedAxes[key] || [];

                // 如果已经选中了该坐标轴，则取消选中
                if (axes.includes(axis)) {
                    this.selectedAxes[key] = axes.filter(a => a !== axis);

                    // 移除与该坐标轴相关的夹角弧线
                    this.editingAngleArcs = this.editingAngleArcs.filter(arc => {
                        return !arc.keypoints || !arc.keypoints.includes(key);
                    });
                } else {
                    // 否则，将该坐标轴添加到选中列表中
                    this.selectedAxes[key] = [...axes, axis];
                }
                
                // 如果已经选中了该坐标轴，则取消选中
                // if (this.selectedAxes.includes(key)) {
                //     this.selectedAxes = this.selectedAxes.filter(a => a !== key);
                // } else {
                //     // 否则，将该坐标轴添加到选中列表中
                //     this.selectedAxes.push(key);
                // }

                // 如果选中了两个关键点并且点击了其中一个关键点的坐标轴，绘制夹角弧线
                if (this.selectedKeypoints.length === 2 && this.selectedAxes[key]?.length > 0) {
                    this.calculateAngleArcsWithAxis(key, axis);
                }
            }
        },

        // 处理虚线点击事件
        // handleLineClick(index) {
        //     if (this.isEditing) {
        //         console.log('Line clicked:', index);

        //         // 将虚线变为实线
        //         this.linesBetweenKeypoints[index].isSolid = true;
        //     }
        // },

        // 处理 ground 直线点击事件
        handleGroundClick() {
            if (this.isEditing) {
                console.log('Ground clicked');

                // this.selectedGround = true;
                // 切换 ground 的选中状态
                this.selectedGround = !this.selectedGround;

                // 如果取消选中 ground，移除与 ground 相关的连线
                if (!this.selectedGround) {
                    this.linesBetweenKeypoints = this.linesBetweenKeypoints.filter(line => line.key2 !== 'ground');
                }

                // 如果选中了一个关键点并且选中了 ground 直线，则绘制一条竖直线
                if (this.selectedKeypoints.length === 1 && this.selectedGround) {
                    const key1 = this.selectedKeypoints[0];
                    const point1 = this.keypoints[key1];
                    const groundY = this.groundLine ? this.groundLine.y1 : null;

                    if (point1 && groundY !== null) {
                        // 添加一条从关键点到 ground 的竖直线
                        this.linesBetweenKeypoints.push({
                            key1: key1,
                            key2: 'ground',
                            x1: point1.x,
                            y1: point1.y,
                            x2: point1.x,
                            y2: groundY,
                            isSolid: false, // 初始为虚线
                            color: '#A3A3A3', // 颜色为 #A3A3A3
                        });
                    }
                }
            }
        },

        // 计算并绘制以两个关键点间连线和坐标轴直线为两边的夹角弧线
        calculateAngleArcsWithAxis(key, axis) {
            // 清空现有的夹角弧线
            // this.editingAngleArcs = [];

            // 获取选中的两个关键点
            const [key1, key2] = this.selectedKeypoints;
            const point1 = this.keypoints[key1];
            const point2 = this.keypoints[key2];

            if (point1 && point2) {
                // 对关键点坐标进行缩放换算
                const scaledPoint1 = {
                    x: this.transformX(point1.x),
                    y: this.transformY(point1.y),
                };
                const scaledPoint2 = {
                    x: this.transformX(point2.x),
                    y: this.transformY(point2.y),
                };

                // 获取点击的坐标轴直线
                const axisLine = this.getAxisLine(key, axis);
                if (!axisLine) return;

                // 计算夹角弧线的路径
                const radius = 20; // 弧线半径
                const startAngle = this.calculateAngleBetweenPoints(scaledPoint2, scaledPoint1);
                const endAngle = this.calculateAngleBetweenPoints(scaledPoint2, { x: axisLine.x2, y: axisLine.y2 });

                // 添加新的夹角弧线
                this.editingAngleArcs.push({
                    d: this.describeArc(scaledPoint2.x, scaledPoint2.y, radius, startAngle, endAngle),
                    color: '#F7877C', // 弧线颜色
                    keypoints: [key1, key2], // 记录关联的关键点
                });
            }
        },

        // 获取坐标轴直线（进行缩放换算）
        getAxisLine(key, axis) {
            const point = this.keypoints[key];
            if (!point) return null;

            const axisLength = 50 * Math.min(this.scaleX, this.scaleY); // 轴线的长度

            // 定义坐标轴直线的起点和终点（未缩放）
            let x1 = point.x;
            let y1 = point.y;
            let x2, y2;

            switch (axis) {
                case 'x':
                    x2 = point.x + axisLength;
                    y2 = point.y;
                    break;
                case 'y':
                    x2 = point.x - axisLength / 1.414;
                    y2 = point.y + axisLength / 1.414;
                    break;
                case 'z':
                    x2 = point.x;
                    y2 = point.y - axisLength;
                    break;
                default:
                    return null;
            }

            // 对起点和终点进行缩放换算
            return {
                x1: this.transformX(x1),
                y1: this.transformY(y1),
                x2: this.transformX(x2),
                y2: this.transformY(y2),
            };

            // switch (axis) {
            //     case 'x':
            //         return {
            //             x1: point.x,
            //             y1: point.y,
            //             x2: point.x + axisLength,
            //             y2: point.y,
            //         };
            //     case 'y':
            //         return {
            //             x1: point.x,
            //             y1: point.y,
            //             x2: point.x - axisLength / 1.414,
            //             y2: point.y + axisLength / 1.414,
            //         };
            //     case 'z':
            //         return {
            //             x1: point.x,
            //             y1: point.y,
            //             x2: point.x,
            //             y2: point.y - axisLength,
            //         };
            //     default:
            //         return null;
            // }
        },
    }
}
</script>

<style scoped>
.constraint-name-text {
    font-size: 15px;
    font-weight: bold;

    margin-top: 5px;
    margin-bottom: 5px;
}

.image-container {
    width: 100%;
    height: 100%;
    /* max-width: 100%; */
    /* max-height: 100%; */
    overflow: hidden;
    /* object-fit: contain; */
    display: flex;
    flex-direction: column;
    /* flex-shrink: 1; */
    align-items: center;
    justify-content: center;

    position: relative;

    padding: 0 10px;
    box-sizing: border-box;
}

.segment-image {
    /* flex: 1; */
    /* height: 0; */
    /* width: 100%; */
    /* height: 100%; */
    /* min-width: 0; */
    /* min-height: 0; */
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.constraint-rectangles {
    position: absolute; /* 绝对定位 */
    top: 15px; /* 距离顶部 10px */
    right: 5px; /* 距离右侧 10px */
    display: flex;
    flex-direction: column;
    gap: 5px; /* 矩形之间的间距 */
}

.constraint-rectangle {
    padding: 5px 10px;
    background-color: #D9D9D9; /* 半透明白色背景 */
    border: 1px solid #ccc;
    border-radius: 2px;
    font-size: 12px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.constraint-rectangle.active {
    background-color: #F7877C; /* 高亮背景色 */
    /* border-color: #000;  */
    /* 高亮边框颜色 */
}

/* .constraint-rectangle.add-button {
    background-color: #F7877C;
    color: white;
    font-weight: bold;
} */

.keypoint {
    position: absolute;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #ffffff; /* 内环白色 */
    border: 3px solid #a3a3a3; /* 外环灰色 */
    transform: translate(-50%, -50%); /* 居中 */
}

.connection-lines {
    position: absolute;
    top: 0;
    left: 0;
    pointer-events: none; /* 防止遮挡点击事件 */
}
</style>