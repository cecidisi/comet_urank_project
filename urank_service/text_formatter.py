class TextFormatter:

	@classmethod
	def get_formatted_word(cls, word, color, decoration):
		if decoration == 'background':
			return "<strong style='border-radius: 4px; font-weight: normal; border: 1px solid "+ color +";background:" + color + "'>" + word + "</strong>"
		else:
			return "<strong style='border-bottom: 1px solid " + color + ";'>" + word + "</strong>"


	@classmethod
	def get_formatted_text(cls, text, kw_positions, kw_colors, decoration, trim=None):
		pretty_text = ''
		highlights = []
		from_positions = {}

		# Add all formatted words to highlights list and then sort from last to first
		for stems, color in kw_colors.iteritems():
			stem_list = stems.split(' ')
			if all([stem in kw_positions for stem in stem_list]):
				for stem in stem_list:
					# Positions for current keyword
					positions = kw_positions[stem] if stem in kw_positions else []
					for pos in positions:
						if not trim or (pos['from_pos'] <= trim and pos['to_pos'] <= trim):
							if pos['from_pos'] not in from_positions:
								word = text[pos['from_pos']:pos['to_pos']]
								highlights.append({
									'styled_word': cls.get_formatted_word(word, color, decoration),
									'from_pos': pos['from_pos'],
									'to_pos': pos['to_pos']
								})
								from_positions[pos['from_pos']] = True
		# Sort all highlights from last to first
		highlights = sorted(highlights, key=lambda h: h['to_pos'])

		if trim:
			original_text = text
			text = text[0:trim]

		last_pos = len(text)
		# Go backwards replacing text
		for h in highlights[::-1]:
			text_after = text[h['to_pos'] : last_pos]
			pretty_text = h['styled_word'] + text_after + pretty_text
			last_pos = h['from_pos']
		pretty_text = text[0:last_pos] + pretty_text

		if trim and len(original_text) > trim:
			pretty_text = pretty_text + '...'
		return pretty_text


