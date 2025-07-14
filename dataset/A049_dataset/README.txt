Given the comprehensive nature of the complete FLAG3D dataset[1], a license agreement is required to apply for permission. Therefore, we have chosen the A049 sub-dataset as an example case to demonstrate the workflow of our dataset preparation and the specific file structure.

Language(instruction.zip): Axxx represents the action of xxx. I001 represents the name of the action, and I002 represents the description of the action. Every action contains the parts above. For some actions, we provided more detailed information.  

Rendering Video: We share a subset of it that contains 1800 videos because of the data size. If you need more, please email us. Sxxx represents the scene of number xxx. Cxxx represents the camera position of number xxx. Mxxx represents the avatar of the number xxx. Pxxx represents the action of person number xxx. Axxx represents the action of xxx. R represents the repeat times of the same action.

Raw Data(raw_data)

Key Attribute.json: •	The term "key attributes" in the context of fitness refers to the essential characteristics that define a specific exercise, particularly focusing on a particular body part. For example, in a sumo squat, the hip trajectory is a key attribute. These attributes describe the primary joint movements and the target muscles involved in the exercise.

Key_Pose Constraints.json: This introduces the relation-ship between key poses (kinematic constraints) we study. Fine-grained classification of kinematic constraints applied in motion chain with an example of A049.

Ground Truth Feedback.json: ground truth feedback for M001P001A049R002.

@inproceedings{flag3d_cvpr,
  title={FLAG3D: A 3D Fitness Activity Dataset with Language Instruction},
  author={Yansong Tang and Jinpeng Liu and Aoyang Liu and Bin Yang and Wenxun Dai and Yongming Rao and Jiwen Lu and Jie Zhou and Xiu Li},
  booktitle={CVPR},
  year={2023},
}      
  