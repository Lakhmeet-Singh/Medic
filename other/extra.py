# def chatbot_response(msg):
#     ints = predict_class(msg, model)
#     intent = ints[0]['intent']
    
#     medical_terms = tokenize_health_question(msg)
#     medicine_terms = tokenize_medicines_question(msg)

#     if intent in ('symptoms', 'additional_detail', 'treatment'):
#         if medical_terms:
#             symptoms_info = get_symptoms_info(medical_terms)

#             if intent == 'symptoms':
#                 name_description = name_description(symptoms_info)
#                 return 'Symptoms name and description: {}'.format(name_description)
#             elif intent == 'additional_detail':
#                 has_part_data = hasPart(symptoms_info)
#                 main_entity_of_page_data = mainEntityOfPage(symptoms_info)

#                 more_info = "Can you provide me with the treatment for - Symptom name"
#                 italic_note_info = markdown.markdown(f'*{more_info}*')
#                 note = "If you require information about treatment, please type your query in the following format: " + italic_note_info

#                 if has_part_data:
#                     title = "Note: "
#                     bold_title = markdown.markdown(f'**{title}**')
#                     info = 'Additional Information: {}'.format(has_part_data)
#                     note_info = bold_title + note
#                     return info + note_info
#                 else:
#                     return 'Additional Information: {} Note: {}'.format(main_entity_of_page_data, note)
#             elif intent == 'treatment':
#                 treatment = treatment_info(symptoms_info)
#                 return 'Treatment: {}'.format(treatment)
#         else:
#             return "Sorry! I couldn't understand you. Could you please rephrase your question?"

#     elif intent in ('medicine', 'medicine_additional_detail'):
#         if medicine_terms:
#             medicine_info = get_medicine_info(medicine_terms)

#             if intent == 'medicine':
#                 name_description_medicine = medicine_name_description(medicine_info)
#                 return 'Medicine name and description: {}'.format(medicine_name_description)
#             elif intent == 'medicine_additional_detail':
#                 additional_detail_medicine = medicine_hasPart(medicine_info)
#                 return 'Additional Information: {}'.format(additional_detail_medicine)
#         else:
#             return "Sorry! I couldn't understand you. Could you please rephrase your question?"
          
#     elif intent == 'pharmacy':
#         return "Which area are you looking the pharmacy in?"
    
#     elif intent == 'pharmacy_follow_up_question':
#         return get_pharmacy_response(msg, pharmacy_intent )

#     else:
#         res = get_standard_response(ints, intents)
#         return res
