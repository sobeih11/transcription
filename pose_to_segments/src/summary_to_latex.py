import csv

# LaTeX table structure
latex_table = r"""
\begin{table*}[htbp]
% \small
\centering
\resizebox{\textwidth}{!}{%
\begin{tabular}{llccc|ccc|cc}
\toprule
 & & \multicolumn{3}{c}{\textbf{Segmentation}} & \multicolumn{3}{c}{\textbf{Segmentation}} & \multicolumn{2}{c}{\textbf{Efficiency}} \\
\cmidrule(lr){3-5} \cmidrule(lr){6-8} \cmidrule(lr){9-10}
\multicolumn{2}{l}{\textbf{Experiment}} & \textbf{F1} & \textbf{IoU} & \textbf{\%} & \textbf{F1} & \textbf{IoU} & \textbf{\%} & \textbf{\#Params} & \textbf{Time} \\
\midrule
"""

with open('./pose_to_segments/src/summary_pro.csv', 'r') as f:
    reader = csv.DictReader(f)  # use DictReader
    for row_dict in reader:
        if row_dict['id'] in ['E1', 'E1s', 'E4ba']:
            latex_table += "\\midrule\n"

        # Remove std
        for k, v in row_dict.items():
            row_dict[k] = v.split('±')[0]
        
        row_dict['test_sign_frame_f1'] = f"${row_dict['test_sign_frame_f1']}$"
        row_dict['test_sentence_frame_f1'] = f"${row_dict['test_sentence_frame_f1']}$"
        row_dict['test_sign_segment_IoU'] = f"${row_dict['test_sign_segment_IoU']}$"
        row_dict['test_sign_segment_percentage'] = f"${row_dict['test_sign_segment_percentage']}$"
        row_dict['test_sentence_segment_percentage'] = f"${row_dict['test_sentence_segment_percentage']}$"
        row_dict['test_sentence_segment_IoU'] = f"${row_dict['test_sentence_segment_IoU']}$"
        
        if row_dict['id'] == 'E0':
            row_dict['test_sign_frame_f1'] = '---'
            row_dict['test_sentence_frame_f1'] = '---'
        
        latex_table += r"\textbf{" + row_dict['id'] + r"} & \textbf{" + row_dict['note'].replace('_', '\\_') + "}" + " & "
        latex_table += row_dict['test_sign_frame_f1'] + " & " + row_dict['test_sign_segment_IoU'] + " & " + row_dict['test_sign_segment_percentage'] + " & "
        latex_table += row_dict['test_sentence_frame_f1'] + " & " + row_dict['test_sentence_segment_IoU'] + " & " + row_dict['test_sentence_segment_percentage'] + " & "
        latex_table += row_dict['#parameters'] + " & " + row_dict['training_time_avg'] + r"\\" + "\n"


latex_table += r"""
\bottomrule
\end{tabular}
}
\caption{Mean test evaluation metrics for our experiments. The best score of each column is in bold. Appendix \ref{appendix:preliminary} contains a complete report including validation metrics and standard deviation of all experiments.}
\label{tab:results}
\end{table*}
"""

# Write the LaTeX table to a .tex file
print(latex_table.replace('±', '\pm'))
