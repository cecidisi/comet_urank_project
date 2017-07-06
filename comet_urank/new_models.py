"""  START My Models  """

#  Colloquium keywords
class ColKeyword(models.Model):
    stem = models.CharField(max_length=45, blank=True, null=True)
    tf = models.IntegerField(blank=True, null=True)
    tfidf = models.FloatField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    is_title = models.IntegerField(blank=True, null=True)
    colloquium = models.ForeignKey(Colloquium, on_delete=models.CASCADE, default='')
    
    class Meta:
        db_table = 'col_keyword'


class KeywordPosTitle(models.Model):
    from_pos = models.IntegerField(blank=True, null=True)
    to_pos = models.IntegerField(blank=True, null=True)
    col_kw = models.ForeignKey(ColKeyword, on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'keyword_pos_title'


class KeywordPosDetail(models.Model):
    from_pos = models.IntegerField(blank=True, null=True)
    to_pos = models.IntegerField(blank=True, null=True)
    col_kw = models.ForeignKey(ColKeyword, on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'keyword_pos_detail'


class GlobalKeywords(models.Model):
    stem = models.CharField(max_length=45, blank=True, null=True)
    term = models.CharField(max_length=45, blank=True, null=True)
    df = models.IntegerField(blank=True, null=True)
    variations = models.TextField()
    colloquia = models.ManyToManyField(Colloquium)
    proxterms = models.ManyToManyField('self', blank=True)
    


# Usertags extracted from userprofiles
class Usertag(models.Model):
    tag = models.CharField(max_length=45, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE, default='')
    colloquia = models.ManyToManyField(Colloquium)
    proxusertags = models.ManyToManyField('self', blank=True)

    class Meta:
        db_table = 'usertag'



"""  END My Models  """
