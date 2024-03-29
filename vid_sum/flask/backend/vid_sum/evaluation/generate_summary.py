import numpy as np
from vid_sum.evaluation.knapsack_implementation import knapsack

def generate_summary(all_shot_bound, all_scores, all_nframes, all_positions, all_fps, duration=-1): 

    all_summaries = []
    for video_idx in range(len(all_scores)):
        shot_bound = all_shot_bound[video_idx]
        frame_init_scores = all_scores[video_idx]
        n_frames = all_nframes[video_idx]
        positions = all_positions[video_idx]
        fps = all_fps[video_idx]

        # Compute the importance scores for the initial frame sequence (not the subsampled one)
        frame_scores = np.zeros((n_frames), dtype=np.float32)
        if positions.dtype != int:
            positions = positions.astype(np.int32)
        if positions[-1] != n_frames:
            positions = np.concatenate([positions, [n_frames]])
        for i in range(len(positions) - 1):
            pos_left, pos_right = positions[i], positions[i+1]
            if i == len(frame_init_scores):
                frame_scores[pos_left:pos_right] = 0
            else:
                frame_scores[pos_left:pos_right] = frame_init_scores[i]

        # Compute shot-level importance scores by taking the average importance scores of all frames in the shot
        shot_imp_scores = []
        shot_lengths = []
        for shot in shot_bound:
            shot_lengths.append(shot[1] - shot[0] + 1)
            shot_imp_scores.append((frame_scores[shot[0]:shot[1] + 1].mean()).item())

        # Select the best shots using the knapsack implementation
        # Calculate number of frames chosen for summary
        if duration != -1:
            final_max_length = int(fps*duration)
        else:
            final_max_length = int((shot[1] + 1)*0.15)

        selected = knapsack(final_max_length, shot_lengths, shot_imp_scores, len(shot_lengths))
        
        # Select all frames from each selected shot (by setting their value in the summary vector to 1)
        summary = np.zeros(shot[1] + 1, dtype=np.int8)
        for shot in selected:
            summary[shot_bound[shot][0]:shot_bound[shot][1] + 1] = 1
        if (np.argwhere(summary == 1).shape[0] < final_max_length):
            temp = final_max_length - np.argwhere(summary == 1).shape[0]
            summary[:temp] = 1
        all_summaries.append(summary)

    return all_summaries