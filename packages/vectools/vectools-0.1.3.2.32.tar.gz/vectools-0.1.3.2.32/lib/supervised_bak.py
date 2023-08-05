'''
if args.predictions:
    with open(args.predictions, 'w') as p_file:
        for el in predictions_vector:
            p_file.write("\t".join(el)+"\n")
'''

'''
for i in range(classifier.n_splits_):
    tmp_train_str = "split%d_train_score" % i
    tmp_test_str = "split%d_test_score" % i

    for j in range(len(cv_results[tmp_train_str])):
        train_el = cv_results[tmp_train_str][j]
        test_el = cv_results[tmp_test_str][j]

if args.predictions:
    preds_matrix_obj = ParseVectors(
        has_col_names=args.column_titles,
        #has_row_names=args.row_titles,
        delimiter=args.delimiter)

    predictions_column_id.append("true_class")
    predictions_column_id.append("model_class")
    predictions_column_id.append("prediction")
    predictions_column_id.append("prediction_score")

    out_file = []
    if len(int_to_name_dict) is 2:
        for i in range(len(testing_predictions)):
            out_file.append([
                str(training_labels[i, 0]),
                str(training_labels[i, 0]),
                str(testing_predictions[i, 0])])
    else:
        for i in range(len(testing_labels[:, 0])):

            true_class = None
            for j in range(len(int_to_name_dict)):  # sorted(int_to_name_dict):
                if testing_labels[i, j] == 1:
                    true_class = j

            for j in range(len(int_to_name_dict)):  # sorted(int_to_name_dict):

                if testing_predictions[i, j] >= 0:
                    tmp_decision = "True"
                else:
                    tmp_decision = "False"

                out_file.append([
                    str(true_class),
                    str(j),
                    tmp_decision,
                    str(testing_predictions[i, j])]
                )

    preds_matrix_obj.out(
        out_file,
        column_titles=predictions_column_id,
        # row_titles=row_testing_labels,
        output_type=args.predictions)
'''

'''
predictions_vector = []
for i in range(len(testing_predictions)):

    prediction_type = "testing"
    prediction_score = str(testing_predictions[i][0])
    true_class_label = str(testing_labels[i])
    predicted_class = "0" if testing_predictions[i] <= 0 else "1"

    if args.row_titles and not args.row_titles_as_classes:
        row_id = row_testing_labels[i]
    else:
        row_id = "None"

    predictions_vector.append(
        [
            prediction_type,
            row_id,
            prediction_score,
            true_class_label,
            predicted_class
        ]
    )

#
for i in range(len(training_predictions)):

    prediction_type = "training"
    prediction_score = str(training_predictions[i][0])
    true_class_label = str(training_labels[i])
    predicted_class = "0" if training_predictions[i] <= 0 else "1"

    if args.row_titles and not args.row_titles_as_classes:
        row_id = row_training_labels[i]
    else:
        row_id = "None"

    predictions_vector.append(
        [
            prediction_type,
            row_id,
            prediction_score,
            true_class_label,
            predicted_class
        ]
    )
'''
# Unfortunately we cannot access the scores from the classifier object
# therefore we predict and compare them to labels here.
# testing_predictions = classifier.decision_function(testing_vectors)
# training_predictions = classifier.decision_function(training_vectors)

# p = precision_score(id_array, y_preds, average='macro')
# p = precision_score(id_array, y_preds, average='micro')
# cm_col_ids = np.array(["actual_classes"] + ["predicted_" + int_to_name_dict[i] for i in sorted(int_to_name_dict)])
# cm_row_ids = np.array(["actual_" + int_to_name_dict[i] for i in sorted(int_to_name_dict)])
'''
predictions_vector = []
for i in range(len(testing_predictions)):

    prediction_type = "testing"
    prediction_score = str(testing_predictions[i][0])
    true_class_label = str(testing_labels[i])
    predicted_class = "0" if testing_predictions[i] <= 0 else "1"

    if args.row_titles and not args.row_titles_as_classes:
        row_id = row_testing_labels[i]
    else:
        row_id = "None"

    predictions_vector.append(
        [
            prediction_type,
            row_id,
            prediction_score,
            true_class_label,
            predicted_class
        ]
    )

#
for i in range(len(training_predictions)):

    prediction_type = "training"
    prediction_score = str(training_predictions[i][0])
    true_class_label = str(training_labels[i])
    predicted_class = "0" if training_predictions[i] <= 0 else "1"

    if args.row_titles and not args.row_titles_as_classes:
        row_id = row_training_labels[i]
    else:
        row_id = "None"

    predictions_vector.append(
        [
            prediction_type,
            row_id,
            prediction_score,
            true_class_label,
            predicted_class
        ]
    )
'''
"""
if args.predictions:
    out_preds = []
    for i in range(len(id_array)):
        out_preds.append(args.delimiter.join(
            [
                int_to_name_dict[id_array[i]].split("/")[-1],
                str(id_array[i]),
                str(y_preds[i])
            ]
        ))
    prediction_files = open(args.predictions, "w")
    prediction_files.write("\n".join(out_preds))
    prediction_files.close()

best_index = classifier.best_index_
cv_results = classifier.cv_results_
best_estimator = classifier.best_estimator_
"""
"""
if len(int_to_name_dict) is 2:
    for class_number in y_preds:
        print(int_to_name_dict[class_number])
else:
    for class_number in y_preds:
        print(int_to_name_dict[class_number])
"""
