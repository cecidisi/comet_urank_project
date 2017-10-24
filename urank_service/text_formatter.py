class TextFormatter:

	@classmethod
	def get_formatted_word(cls, word, color, decoration):
		if decoration == 'background':
			return "<strong style='border-radius: 4px; font-weight: normal; border: 1px solid "+ color +";background:" + color + "'>" + word + "</strong>"
		else:
			return "<strong style='border-bottom: 1px solid " + color + ";'>" + word + "</strong>"


	@classmethod
	def get_formatted_text(cls, text, kw_positions, kw_colors, decoration):
		pretty_text = ''
		highlights = []
		# Add all formatted words to highlights list and then sort from last to first
		for stems, color in kw_colors.iteritems():
			for stem in stems.split(' '):
				# Positions for current keyword
				positions = kw_positions[stem] if stem in kw_positions else []
				for pos in positions:
					word = text[pos['from_pos']:pos['to_pos']]
					highlights.append({
						'styled_word': cls.get_formatted_word(word, color, decoration),
						'from_pos': pos['from_pos'],
						'to_pos': pos['to_pos']
					})
		# Sort all highlights from last to first
		highlights = sorted(highlights, key=lambda h: h['to_pos'])
		last_pos = len(text)
		# Go backwards replacing text
		for h in highlights[::-1]:
			text_after = text[h['to_pos'] : last_pos]
			pretty_text = h['styled_word'] + text_after + pretty_text
			last_pos = h['from_pos']

		return text[0:last_pos] + pretty_text