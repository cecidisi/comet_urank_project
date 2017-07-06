# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    like_date = models.DateTimeField()
    user_id = models.IntegerField()
    unliked = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = '_like'


class Adaptmessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    message = models.TextField()

    class Meta:
        managed = False
        db_table = 'adaptmessage'


class Affiliate(models.Model):
    affiliate_id = models.AutoField(primary_key=True)
    affiliate = models.CharField(max_length=450)

    class Meta:
        managed = False
        db_table = 'affiliate'
        unique_together = (('affiliate_id', 'affiliate'),)


class AffiliateCol(models.Model):
    ac_id = models.AutoField(primary_key=True)
    affiliate_id = models.IntegerField()
    col_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'affiliate_col'


class AffiliateColCopy(models.Model):
    ac_id = models.AutoField(primary_key=True)
    affiliate_id = models.IntegerField()
    col_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'affiliate_col_copy'


class AffiliateSeries(models.Model):
    as_id = models.AutoField(primary_key=True)
    affiliate_id = models.IntegerField()
    series_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'affiliate_series'


class AffiliateUser(models.Model):
    au_id = models.AutoField(primary_key=True)
    affiliate_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'affiliate_user'


class AffiliateUserCopy(models.Model):
    au_id = models.AutoField(primary_key=True)
    affiliate_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'affiliate_user_copy'


class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    agency = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area'


class AreaCol(models.Model):
    area_col_id = models.AutoField(primary_key=True)
    area_id = models.IntegerField()
    col_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area_col'


class AreaColCopy(models.Model):
    area_col_id = models.AutoField(primary_key=True)
    area_id = models.IntegerField()
    col_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area_col_copy'


class AreaSeries(models.Model):
    area_series_id = models.AutoField(primary_key=True)
    area_id = models.IntegerField()
    series_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area_series'


class CleanCol(models.Model):
    col_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=400)
    detail = models.TextField()
    cleantime = models.DateTimeField()
    detail_all = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clean_col'


class CleanColScinet(models.Model):
    col_id = models.AutoField(primary_key=True)
    title = models.TextField()
    detail = models.TextField()
    cleantime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'clean_col_scinet'


class CleanColUserstudy(models.Model):
    col_id = models.AutoField(primary_key=True)
    title = models.TextField()
    detail = models.TextField()
    cleantime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'clean_col_userstudy'


class ClusterUser(models.Model):
    cu_id = models.AutoField(primary_key=True)
    cluster_method_id = models.IntegerField()
    cluster_date = models.DateTimeField()
    numcluster = models.IntegerField(db_column='numCluster')  # Field name made lowercase.
    numiteration = models.IntegerField(db_column='numIteration')  # Field name made lowercase.
    numrepeat = models.IntegerField(db_column='numRepeat')  # Field name made lowercase.
    bic = models.FloatField()

    class Meta:
        managed = False
        db_table = 'cluster_user'


class ClusterUserMember(models.Model):
    cum_id = models.AutoField(primary_key=True)
    cu_id = models.IntegerField()
    clusterno = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cluster_user_member'


class ColBk(models.Model):
    col_bk_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    col_id = models.IntegerField()
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.
    begintime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=300)
    detail = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    title = models.CharField(max_length=400)
    user_id = models.IntegerField()
    speaker_id = models.IntegerField()
    host_id = models.IntegerField()
    url = models.CharField(max_length=400, blank=True, null=True)
    owner_id = models.IntegerField(blank=True, null=True)
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slide_url = models.CharField(max_length=500, blank=True, null=True)
    s_bio = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'col_bk'


class ColDetailChunk(models.Model):
    cdc_id = models.AutoField(primary_key=True)
    sentence_original = models.TextField()
    sentence_parsed = models.TextField()
    pos = models.IntegerField()
    is_col_desc_man = models.IntegerField(blank=True, null=True)
    is_col_desc_aut = models.IntegerField(blank=True, null=True)
    fcol = models.ForeignKey('Colloquium', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'col_detail_chunk'


class ColImpact(models.Model):
    ciid = models.AutoField(db_column='ciID', primary_key=True)  # Field name made lowercase.
    col_id = models.IntegerField()
    viewno = models.IntegerField()
    bookmarkno = models.IntegerField()
    emailno = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'col_impact'


class ColImpactScinet(models.Model):
    ciid = models.AutoField(db_column='ciID', primary_key=True)  # Field name made lowercase.
    col_id = models.IntegerField(unique=True)
    viewno = models.IntegerField()
    bookmarkno = models.IntegerField()
    emailno = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'col_impact_scinet'


class ColRank(models.Model):
    comm_id = models.IntegerField(primary_key=True)
    col_id = models.IntegerField()
    score = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'col_rank'
        unique_together = (('comm_id', 'col_id'),)


class ColSpeaker(models.Model):
    cs_id = models.AutoField(primary_key=True)
    col_id = models.IntegerField()
    speaker_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'col_speaker'


class ColSpeakerCopy(models.Model):
    cs_id = models.AutoField(primary_key=True)
    col_id = models.IntegerField()
    speaker_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'col_speaker_copy'



class Coldistance(models.Model):
    cd_id = models.AutoField(primary_key=True)
    col0_id = models.IntegerField()
    col1_id = models.IntegerField()
    ngram = models.IntegerField()
    distance = models.FloatField()
    caldate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'coldistance'


class Colkmedroid(models.Model):
    ckm_id = models.AutoField(primary_key=True)
    cluster = models.IntegerField()
    ngram = models.IntegerField()
    costfn = models.CharField(max_length=100)
    round = models.IntegerField()
    medroid = models.IntegerField()
    col_id = models.IntegerField()
    clustertime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'colkmedroid'


class Colloquium(models.Model):
    col_id = models.AutoField(primary_key=True)
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.
    begintime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=300)
    detail = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    title = models.CharField(max_length=400)
    user_id = models.IntegerField()
    speaker_id = models.IntegerField()
    host_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=400, blank=True, null=True)
    owner_id = models.IntegerField()
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slide_url = models.CharField(max_length=500, blank=True, null=True)
    paper_url = models.CharField(max_length=500, blank=True, null=True)
    s_bio = models.TextField(blank=True, null=True)
    concattitle = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'colloquium'


class ColloquiumCopy(models.Model):
    col_id = models.AutoField(primary_key=True)
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.
    begintime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=300)
    detail = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    title = models.CharField(max_length=400)
    user_id = models.IntegerField()
    speaker_id = models.IntegerField()
    host_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=400, blank=True, null=True)
    owner_id = models.IntegerField()
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slide_url = models.CharField(max_length=500, blank=True, null=True)
    paper_url = models.CharField(max_length=500, blank=True, null=True)
    s_bio = models.TextField(blank=True, null=True)
    state = models.IntegerField()
    concattitle = models.CharField(max_length=400, blank=True, null=True)
    sourcecrawler = models.CharField(max_length=400, blank=True, null=True)
    originalseries = models.CharField(max_length=400, blank=True, null=True)
    originalsponsor = models.CharField(max_length=400, blank=True, null=True)
    existing_col_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colloquium_copy'


class ColloquiumExpBookmarking(models.Model):
    col_id = models.AutoField(primary_key=True)
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.
    begintime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=300)
    detail = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    title = models.CharField(max_length=400)
    user_id = models.IntegerField()
    speaker_id = models.IntegerField()
    host_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=400, blank=True, null=True)
    owner_id = models.IntegerField()
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slide_url = models.CharField(max_length=500, blank=True, null=True)
    paper_url = models.CharField(max_length=500, blank=True, null=True)
    s_bio = models.TextField(blank=True, null=True)
    concattitle = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colloquium_exp_bookmarking'


class ColloquiumExpRating(models.Model):
    col_id = models.AutoField(primary_key=True)
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.
    begintime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=300)
    detail = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    title = models.CharField(max_length=400)
    user_id = models.IntegerField()
    speaker_id = models.IntegerField()
    host_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=400, blank=True, null=True)
    owner_id = models.IntegerField()
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slide_url = models.CharField(max_length=500, blank=True, null=True)
    paper_url = models.CharField(max_length=500, blank=True, null=True)
    s_bio = models.TextField(blank=True, null=True)
    concattitle = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colloquium_exp_rating'


class ColloquiumExpTrainingBookmarking(models.Model):
    col_id = models.AutoField(primary_key=True)
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.
    begintime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=300)
    detail = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    title = models.CharField(max_length=400)
    user_id = models.IntegerField()
    speaker_id = models.IntegerField()
    host_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=400, blank=True, null=True)
    owner_id = models.IntegerField()
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slide_url = models.CharField(max_length=500, blank=True, null=True)
    paper_url = models.CharField(max_length=500, blank=True, null=True)
    s_bio = models.TextField(blank=True, null=True)
    concattitle = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colloquium_exp_training_bookmarking'


class ColloquiumExpTrainingRating(models.Model):
    col_id = models.AutoField(primary_key=True)
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.
    begintime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=300)
    detail = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    title = models.CharField(max_length=400)
    user_id = models.IntegerField()
    speaker_id = models.IntegerField()
    host_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=400, blank=True, null=True)
    owner_id = models.IntegerField()
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slide_url = models.CharField(max_length=500, blank=True, null=True)
    paper_url = models.CharField(max_length=500, blank=True, null=True)
    s_bio = models.TextField(blank=True, null=True)
    concattitle = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colloquium_exp_training_rating'


class ColloquiumScinet(models.Model):
    col_id = models.AutoField(primary_key=True)
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.
    begintime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=300)
    detail = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    title = models.CharField(max_length=400)
    user_id = models.IntegerField()
    speaker_id = models.IntegerField()
    host_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=400, blank=True, null=True)
    owner_id = models.IntegerField()
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slide_url = models.CharField(max_length=500, blank=True, null=True)
    paper_url = models.CharField(max_length=500, blank=True, null=True)
    s_bio = models.TextField(blank=True, null=True)
    concattitle = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colloquium_scinet'


class Colterm(models.Model):
    ct_id = models.AutoField(primary_key=True)
    col_id = models.IntegerField()
    termtype = models.CharField(max_length=20)
    term = models.CharField(max_length=100)
    freq = models.IntegerField()
    ngram = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'colterm'


class ColtermScinet(models.Model):
    ct_id = models.AutoField(primary_key=True)
    col_id = models.IntegerField()
    termtype = models.CharField(max_length=20)
    term = models.CharField(max_length=100)
    freq = models.IntegerField()
    ngram = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'colterm_scinet'


class ColtermUserstudy(models.Model):
    ct_id = models.AutoField(primary_key=True)
    col_id = models.IntegerField()
    termtype = models.CharField(max_length=20)
    term = models.CharField(max_length=100)
    freq = models.IntegerField()
    ngram = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'colterm_userstudy'


class Coltopic(models.Model):
    ct_id = models.AutoField(primary_key=True)
    col_id = models.IntegerField()
    t_id = models.IntegerField()
    topicdist = models.FloatField()

    class Meta:
        managed = False
        db_table = 'coltopic'


class Cometrecommendations(models.Model):
    user_id = models.IntegerField()
    col_id = models.IntegerField()
    distance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cometrecommendations'


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField()
    comment_date = models.DateTimeField()
    user_id = models.IntegerField()
    uncommented = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'comment'
        unique_together = (('comment_id', 'comment_date', 'user_id', 'uncommented'),)


class CommentCol(models.Model):
    cc_id = models.AutoField(primary_key=True)
    comment_id = models.IntegerField()
    col_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment_col'
        unique_together = (('comment_id', 'col_id'), ('cc_id', 'col_id', 'comment_id'),)


class CommentComment(models.Model):
    cc_id = models.AutoField(primary_key=True)
    comment_id = models.IntegerField()
    commentee_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment_comment'
        unique_together = (('comment_id', 'commentee_id'), ('cc_id', 'commentee_id', 'comment_id'),)


class CommentCommunity(models.Model):
    cc_id = models.AutoField(primary_key=True)
    comment_id = models.IntegerField()
    comm_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment_community'
        unique_together = (('comment_id', 'comm_id'), ('cc_id', 'comm_id', 'comment_id'),)


class CommentEntity(models.Model):
    ce_id = models.AutoField(primary_key=True)
    comment_id = models.IntegerField()
    entity_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment_entity'
        unique_together = (('ce_id', 'entity_id', 'comment_id'),)


class CommentHost(models.Model):
    ch_id = models.AutoField(primary_key=True)
    comment_id = models.IntegerField()
    host_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment_host'
        unique_together = (('ch_id', 'host_id', 'comment_id'),)


class CommentSeries(models.Model):
    cs_id = models.AutoField(primary_key=True)
    comment_id = models.IntegerField()
    series_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment_series'
        unique_together = (('cs_id', 'series_id', 'comment_id'),)


class CommentSpeaker(models.Model):
    cs_id = models.AutoField(primary_key=True)
    comment_id = models.IntegerField()
    speaker_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment_speaker'
        unique_together = (('cs_id', 'speaker_id', 'comment_id'),)


class CommentUser(models.Model):
    cu_id = models.AutoField(primary_key=True)
    comment_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment_user'
        unique_together = (('comment_id', 'user_id'), ('cu_id', 'user_id', 'comment_id'),)


class Commfeedback(models.Model):
    cfb_id = models.AutoField(primary_key=True)
    comm_id = models.IntegerField()
    user_id = models.IntegerField()
    col_id = models.IntegerField()
    rating = models.FloatField()
    ratingtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'commfeedback'


class Community(models.Model):
    comm_id = models.AutoField(primary_key=True)
    comm_name = models.CharField(max_length=200)
    comm_desc = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    user_id = models.IntegerField()
    owner_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'community'
        unique_together = (('comm_id', 'comm_name', 'lastupdate', 'user_id', 'owner_id'),)


class CommunityBk(models.Model):
    comm_id_bk = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    comm_id = models.IntegerField()
    comm_name = models.CharField(max_length=200)
    comm_desc = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    user_id = models.IntegerField()
    owner_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'community_bk'


class Contribute(models.Model):
    contribute_id = models.AutoField(primary_key=True)
    userprofile_id = models.IntegerField(blank=True, null=True)
    comm_id = models.IntegerField()
    lastupdate = models.DateTimeField()
    user_id = models.IntegerField(blank=True, null=True)
    col_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contribute'
        unique_together = (('comm_id', 'user_id', 'col_id'),)


class ContributeVote(models.Model):
    cv_id = models.IntegerField(primary_key=True)
    comm_id = models.IntegerField()
    user_id = models.IntegerField()
    col_id = models.IntegerField()
    vote = models.IntegerField()
    votetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'contribute_vote'


class Discipline(models.Model):
    d_id = models.AutoField(primary_key=True)
    discipline = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'discipline'


class Emailfriends(models.Model):
    ef_id = models.AutoField(primary_key=True)
    col_id = models.IntegerField()
    user_id = models.IntegerField()
    emails = models.CharField(max_length=400)
    timesent = models.DateTimeField()
    message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emailfriends'


class Entities(models.Model):
    entities_id = models.AutoField(primary_key=True)
    entity_id = models.IntegerField()
    relevance = models.FloatField(blank=True, null=True)
    occur = models.IntegerField(blank=True, null=True)
    col_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'entities'
        unique_together = (('entities_id', 'entity_id', 'col_id'),)


class Entity(models.Model):
    entity_id = models.AutoField(primary_key=True)
    entity = models.CharField(max_length=400)
    field_type = models.CharField(db_column='_type', max_length=100)  # Field renamed because it started with '_'.
    normalized = models.CharField(max_length=400, blank=True, null=True)
    other = models.CharField(max_length=200, blank=True, null=True)
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'entity'


class EvaRecUser(models.Model):
    ru_id = models.AutoField(primary_key=True)
    profile_date = models.DateTimeField()
    rec_method_id = models.IntegerField()
    user_id = models.IntegerField()
    col_id = models.IntegerField()
    weight = models.FloatField()
    rec_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'eva_rec_user'


class EvaRecUserKnn(models.Model):
    ruk_id = models.AutoField(primary_key=True)
    ru_id = models.IntegerField()
    col_id = models.IntegerField()
    weight = models.FloatField()

    class Meta:
        managed = False
        db_table = 'eva_rec_user_knn'
        unique_together = (('ru_id', 'col_id', 'weight'),)


class ExtFriend(models.Model):
    ext_friend_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    friend_name = models.CharField(max_length=100, blank=True, null=True)
    updatetime = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_friend'


class ExtFriendCol(models.Model):
    ext_f_col_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    col_id = models.IntegerField(blank=True, null=True)
    friend_name = models.CharField(max_length=100, blank=True, null=True)
    updatetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_friend_col'


class Extmapping(models.Model):
    extmapping_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    ext_id = models.IntegerField()
    exttable = models.CharField(max_length=100)
    mappedtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'extmapping'
        unique_together = (('user_id', 'ext_id', 'exttable'),)


class FailLocation(models.Model):
    col_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'fail_location'


class Friend(models.Model):
    friend_id = models.AutoField(primary_key=True)
    user0_id = models.IntegerField()
    user1_id = models.IntegerField()
    friendtime = models.DateTimeField()
    breaktime = models.DateTimeField(blank=True, null=True)
    breaker_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'friend'
        unique_together = (('friend_id', 'user0_id', 'user1_id'),)


class Friendrequestnotified(models.Model):
    un_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    notified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'friendrequestnotified'


class Friendrequestnum(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'friendrequestnum'


class Friendrequesttemp(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    num = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'friendrequesttemp'


class Friendtalksnum(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'friendtalksnum'


class FriendtalksnumTemp(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'friendtalksnum_temp'


class Gooduserratings(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    col_id = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gooduserratings'


class Grouptalksnum(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'grouptalksnum'


class GrouptalksnumTemp(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'grouptalksnum_temp'


class Host(models.Model):
    host_id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=400)
    hostconcat = models.CharField(max_length=400)
    notrealperson = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'host'


class LastUfbId(models.Model):
    field_ufb_id = models.IntegerField(db_column='_ufb_id', blank=True, null=True)  # Field renamed because it started with '_'.
    user_id = models.IntegerField(blank=True, null=True)
    col_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'last_ufb_id'


class Lastfriendrequestnotified(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_date = models.DateTimeField(db_column='_date', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'lastfriendrequestnotified'


class Lastuserfeedback(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    col_id = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    ratingtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lastuserfeedback'


class Lastusernotified(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_date = models.DateTimeField(db_column='_date', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'lastusernotified'


class LdaHybridTopic(models.Model):
    lt_id = models.AutoField(primary_key=True)
    rawfile = models.CharField(max_length=200)
    numtopics = models.IntegerField()
    alpha = models.FloatField()
    beta = models.FloatField()
    numiterations = models.IntegerField()
    ngram = models.IntegerField()
    estimatetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'lda_hybrid_topic'
        unique_together = (('rawfile', 'numtopics', 'alpha', 'beta', 'numiterations', 'ngram'),)


class LikeComment(models.Model):
    lc_id = models.AutoField(primary_key=True)
    like_id = models.IntegerField()
    comment_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'like_comment'
        unique_together = (('like_id', 'comment_id'), ('lc_id', 'comment_id', 'like_id'),)


class LikeEntity(models.Model):
    le_id = models.AutoField(primary_key=True)
    like_id = models.IntegerField()
    entity_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'like_entity'
        unique_together = (('le_id', 'entity_id', 'like_id'),)


class LikeHost(models.Model):
    lh_id = models.AutoField(primary_key=True)
    like_id = models.IntegerField()
    host_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'like_host'
        unique_together = (('lh_id', 'host_id', 'like_id'),)


class LikeSeries(models.Model):
    ls_id = models.AutoField(primary_key=True)
    like_id = models.IntegerField()
    series_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'like_series'
        unique_together = (('ls_id', 'series_id', 'like_id'),)


class LikeSpeaker(models.Model):
    ls_id = models.AutoField(primary_key=True)
    like_id = models.IntegerField()
    speaker_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'like_speaker'
        unique_together = (('ls_id', 'speaker_id', 'like_id'),)


class LocCol(models.Model):
    lcid = models.AutoField(primary_key=True)
    col_id = models.IntegerField()
    abbr = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loc_col'


class Location(models.Model):
    loc_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'


class LocationCol(models.Model):
    col_loc_id = models.AutoField(primary_key=True)
    col_id = models.IntegerField(blank=True, null=True)
    loc_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_col'


class LocationColCopy(models.Model):
    col_loc_id = models.AutoField(primary_key=True)
    col_id = models.IntegerField(blank=True, null=True)
    loc_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_col_copy'


class LocationCopy(models.Model):
    loc_id = models.AutoField(primary_key=True)
    location = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_copy'


class Member(models.Model):
    m_id = models.AutoField(primary_key=True)
    member_date = models.DateTimeField()
    user_id = models.IntegerField()
    unmembered = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'member'
        unique_together = (('m_id', 'member_date', 'user_id', 'unmembered'),)


class MemberCommunity(models.Model):
    mc_id = models.AutoField(primary_key=True)
    m_id = models.IntegerField()
    comm_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'member_community'
        unique_together = (('m_id', 'comm_id'),)


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    recipient = models.CharField(max_length=400)
    content = models.TextField()
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'message'


class Mobilemapping(models.Model):
    mm_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    mobileno = models.CharField(max_length=95, blank=True, null=True)
    macaddress = models.CharField(max_length=45, blank=True, null=True)
    isandroid = models.IntegerField(db_column='isAndroid', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mobilemapping'


class Opencalais(models.Model):
    opencalais_id = models.AutoField(primary_key=True)
    col_id = models.IntegerField()
    content = models.TextField()
    output = models.TextField()
    field_date = models.DateTimeField(db_column='_date')  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'opencalais'


class Qynewnotewhocommentsonwhom(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'qynewnotewhocommentsonwhom'


class Qynewnotificationno(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'qynewnotificationno'


class Rawcolposttime(models.Model):
    col_id = models.IntegerField(blank=True, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rawcolposttime'


class Rawuserprofiles(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    col_id = models.IntegerField(blank=True, null=True)
    entity_id = models.IntegerField(blank=True, null=True)
    relevance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rawuserprofiles'


class RecComm(models.Model):
    rc_id = models.AutoField(primary_key=True)
    rec_method_id = models.IntegerField()
    comm_id = models.IntegerField()
    col_id = models.IntegerField()
    weight = models.FloatField()
    rec_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rec_comm'


class RecUser(models.Model):
    ru_id = models.AutoField(primary_key=True)
    rec_method_id = models.IntegerField()
    user_id = models.IntegerField()
    col_id = models.IntegerField()
    weight = models.FloatField()
    rec_date = models.DateTimeField()
    rating = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rec_user'


class RecUserKnn(models.Model):
    ruk_id = models.AutoField(primary_key=True)
    ru_id = models.IntegerField()
    col_id = models.IntegerField()
    weight = models.FloatField()

    class Meta:
        managed = False
        db_table = 'rec_user_knn'
        unique_together = (('ru_id', 'col_id', 'weight'),)


class Relation(models.Model):
    relation_id = models.AutoField(primary_key=True)
    parent_id = models.IntegerField(blank=True, null=True)
    child_id = models.IntegerField()
    lvl = models.IntegerField()
    path = models.CharField(max_length=500, blank=True, null=True)
    fullpath = models.CharField(db_column='fullPath', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'relation'
        unique_together = (('relation_id', 'parent_id', 'child_id'),)


class Request(models.Model):
    request_id = models.AutoField(primary_key=True)
    requester_id = models.IntegerField()
    target_id = models.IntegerField()
    requesttime = models.DateTimeField()
    accepttime = models.DateTimeField(blank=True, null=True)
    notnowtime = models.DateTimeField(blank=True, null=True)
    rejecttime = models.DateTimeField(blank=True, null=True)
    droprequesttime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request'
        unique_together = (('request_id', 'requester_id', 'target_id'),)


class Series(models.Model):
    series_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=400)
    description = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    user_id = models.IntegerField()
    semester = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=400, blank=True, null=True)
    owner_id = models.IntegerField()
    contactname = models.CharField(max_length=100, blank=True, null=True)
    contactemail = models.CharField(max_length=100, blank=True, null=True)
    contactno = models.CharField(max_length=100, blank=True, null=True)
    iswebinar = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'series'
        unique_together = (('series_id', 'name', 'user_id', 'owner_id'),)


class SeriesAlias(models.Model):
    series_alias_id = models.AutoField(primary_key=True)
    series_id = models.IntegerField()
    name = models.CharField(max_length=400)
    lastupdate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'series_alias'


class SeriesBk(models.Model):
    series_bk_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    series_id = models.IntegerField()
    name = models.CharField(max_length=400)
    description = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField()
    user_id = models.IntegerField()
    semester = models.IntegerField()
    url = models.CharField(max_length=400, blank=True, null=True)
    owner_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'series_bk'


class SeriesSemester(models.Model):
    ss_id = models.AutoField(primary_key=True)
    series_id = models.IntegerField()
    semester = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'series_semester'


class Seriescol(models.Model):
    seriescol_id = models.AutoField(primary_key=True)
    series_id = models.IntegerField()
    col_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'seriescol'


class SeriescolCopy(models.Model):
    seriescol_id = models.AutoField(primary_key=True)
    series_id = models.IntegerField()
    col_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'seriescol_copy'


class Seriestalksnum(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'seriestalksnum'


class SeriestalksnumTemp(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'seriestalksnum_temp'


class Speaker(models.Model):
    speaker_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    concatname = models.CharField(max_length=250)
    affiliation = models.CharField(max_length=700, blank=True, null=True)
    publications = models.IntegerField(blank=True, null=True)
    citations = models.IntegerField(blank=True, null=True)
    hindex = models.IntegerField(blank=True, null=True)
    gslink = models.CharField(max_length=400, blank=True, null=True)
    picurl = models.CharField(db_column='picURL', max_length=400, blank=True, null=True)  # Field name made lowercase.
    lastupdate = models.DateTimeField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    notrealperson = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'speaker'


class SpeakerAcademicProfile(models.Model):
    uapi_id = models.AutoField(primary_key=True)
    speaker_id = models.IntegerField()
    profileid = models.CharField(db_column='profileID', max_length=50)  # Field name made lowercase.
    profilesource = models.IntegerField(db_column='profileSource')  # Field name made lowercase.
    url = models.CharField(max_length=300, blank=True, null=True)
    imageurl = models.CharField(db_column='imageUrl', max_length=300, blank=True, null=True)  # Field name made lowercase.
    interests = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    crawlingdate = models.DateTimeField(db_column='crawlingDate', blank=True, null=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='checkDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'speaker_academic_profile'
        unique_together = (('speaker_id', 'profileid', 'profilesource'),)


class SpeakerCoAuthorGScholar(models.Model):
    coa_id = models.AutoField(primary_key=True)
    speaker_id = models.IntegerField()
    co_author_name = models.CharField(max_length=100)
    profileid = models.CharField(db_column='profileID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    co_author_speaker_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'speaker_co_author_g_scholar'


class SpeakerExtmapping(models.Model):
    extmapping_id = models.AutoField(primary_key=True)
    speaker_id = models.IntegerField()
    ext_id = models.IntegerField()
    exttable = models.CharField(max_length=100)
    mappedtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'speaker_extmapping'
        unique_together = (('speaker_id', 'ext_id', 'exttable'),)


class SpeakerScopusAuthorMapping(models.Model):
    ss_id = models.AutoField(primary_key=True)
    speaker_id = models.IntegerField()
    scopusauthorid = models.CharField(db_column='scopusAuthorID', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'speaker_scopus_author_mapping'


class SpeakerScopusAuthorSearching(models.Model):
    ss_id = models.AutoField(primary_key=True)
    speaker_id = models.IntegerField()
    scopusauthorid = models.CharField(db_column='scopusAuthorID', max_length=20)  # Field name made lowercase.
    confirmed = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'speaker_scopus_author_searching'


class Subscribe(models.Model):
    s_id = models.AutoField(primary_key=True)
    subscribe_date = models.DateTimeField()
    user_id = models.IntegerField()
    unsubscribed = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'subscribe'
        unique_together = (('s_id', 'subscribe_date', 'user_id', 'unsubscribed'),)


class SubscribeAffiliate(models.Model):
    sa_id = models.AutoField(primary_key=True)
    s_id = models.IntegerField()
    affiliate_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subscribe_affiliate'
        unique_together = (('s_id', 'affiliate_id'), ('sa_id', 'affiliate_id', 's_id'),)


class SubscribeCommunity(models.Model):
    sc_id = models.AutoField(primary_key=True)
    s_id = models.IntegerField()
    comm_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subscribe_community'
        unique_together = (('s_id', 'comm_id'), ('sc_id', 'comm_id', 's_id'),)


class SubscribeSeries(models.Model):
    ss_id = models.AutoField(primary_key=True)
    s_id = models.IntegerField()
    series_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subscribe_series'
        unique_together = (('s_id', 'series_id'), ('ss_id', 'series_id', 's_id'),)


class SubscribeSpeaker(models.Model):
    ss_id = models.AutoField(primary_key=True)
    s_id = models.IntegerField()
    speaker_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subscribe_speaker'
        unique_together = (('s_id', 'speaker_id'), ('ss_id', 'speaker_id', 's_id'),)


class Subspeakernum(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'subspeakernum'


class SubspeakernumTemp(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'subspeakernum_temp'


class Sumuserentities(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    sumrelevance = models.FloatField(db_column='sumRelevance', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sumuserentities'


class SysConfig(models.Model):
    sysid = models.AutoField(db_column='sysId', primary_key=True)  # Field name made lowercase.
    currsemester = models.IntegerField()
    beginterm = models.DateTimeField()
    endterm = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sys_config'


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=100)
    lastupdate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tag'


class Tags(models.Model):
    tags_id = models.AutoField(primary_key=True)
    userprofile_id = models.IntegerField(blank=True, null=True)
    tag_id = models.IntegerField()
    lastupdate = models.DateTimeField()
    user_id = models.IntegerField(blank=True, null=True)
    col_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'


class Talkview(models.Model):
    talkview_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    viewtime = models.DateTimeField(db_column='viewTime')  # Field name made lowercase.
    col_id = models.IntegerField()
    ipaddress = models.CharField(max_length=45, blank=True, null=True)
    sessionid = models.CharField(max_length=95, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'talkview'


class Term(models.Model):
    term_id = models.AutoField(primary_key=True)
    term = models.CharField(max_length=100)
    ngram = models.IntegerField()
    addtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'term'
        unique_together = (('term', 'term_id', 'ngram'),)


class TermLdaHybridTopic(models.Model):
    tlt_id = models.AutoField(primary_key=True)
    lt_id = models.IntegerField()
    topic_no = models.IntegerField()
    term_id = models.IntegerField()
    weight = models.FloatField()
    estimatetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'term_lda_hybrid_topic'
        unique_together = (('lt_id', 'term_id', 'topic_no', 'tlt_id'),)


class TermUserstudyBookmarking(models.Model):
    term = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'term_userstudy_bookmarking'


class Termtopic(models.Model):
    tt_id = models.AutoField(primary_key=True)
    t_id = models.IntegerField()
    term_id = models.IntegerField()
    weight = models.FloatField()
    estimatetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'termtopic'


class Tmpscopuspubid(models.Model):
    said = models.IntegerField(db_column='saID')  # Field name made lowercase.
    spid = models.IntegerField(db_column='spID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tmpScopusPubID'
        unique_together = (('spid', 'said'), ('spid', 'said'),)


class TmpCoaCoAuthor(models.Model):
    coa_id = models.IntegerField(primary_key=True)
    co_author_speaker_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tmp_coa_co_author'
        unique_together = (('coa_id', 'co_author_speaker_id'),)


class TmpScopusSpeakerMapping(models.Model):
    speaker_id = models.IntegerField(primary_key=True)
    said = models.IntegerField(db_column='saID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tmp_scopus_speaker_mapping'
        unique_together = (('speaker_id', 'said'),)


class TmpSpeakerExtmapping(models.Model):
    speaker_id = models.IntegerField(primary_key=True)
    ext_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tmp_speaker_extmapping'
        unique_together = (('speaker_id', 'ext_id'), ('speaker_id', 'ext_id'),)


class TmpSpeakerGscholarAuthor(models.Model):
    speaker_id = models.IntegerField(primary_key=True)
    gsaid = models.IntegerField(db_column='gsaID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tmp_speaker_gscholar_author'
        unique_together = (('speaker_id', 'gsaid'), ('speaker_id', 'gsaid'),)


class Topic(models.Model):
    t_id = models.AutoField(primary_key=True)
    numtopics = models.IntegerField()
    alpha = models.FloatField()
    beta = models.FloatField()
    numiterations = models.IntegerField()
    ngram = models.IntegerField()
    topic_no = models.IntegerField()
    estimatetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'topic'


class UserCiteulikeMapping(models.Model):
    ucm_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    personid = models.IntegerField(db_column='personID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_citeulike_mapping'
        unique_together = (('user_id', 'personid'),)


class UserColValidate(models.Model):
    user_id = models.IntegerField(primary_key=True)
    col_id = models.IntegerField()
    bookmarked = models.TextField()  # This field type is a guess.
    host_id = models.IntegerField()
    speaker_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_col_validate'
        unique_together = (('user_id', 'col_id', 'bookmarked', 'host_id', 'speaker_id'), ('user_id', 'col_id', 'bookmarked', 'host_id', 'speaker_id'),)


class UserCommunity(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    comm_id = models.IntegerField(blank=True, null=True)
    comm_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_community'


class UserHomePage(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=50)
    page_kind = models.IntegerField()
    group = models.IntegerField()
    series = models.IntegerField()
    icon = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_home_page'
        unique_together = (('user_id', 'email', 'timestamp'),)


class UserLdaHybridTopic(models.Model):
    clt_id = models.AutoField(primary_key=True)
    instance_id = models.CharField(max_length=50)
    lt_id = models.IntegerField()
    topic_no = models.IntegerField()
    topicdist = models.FloatField()

    class Meta:
        managed = False
        db_table = 'user_lda_hybrid_topic'
        unique_together = (('instance_id', 'lt_id', 'topic_no', 'topicdist'),)


class UserMessage(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=50)
    message_id = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_message'
        unique_together = (('user_id', 'email', 'timestamp'),)


class UserScopusAuthorMapping(models.Model):
    us_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    scopusauthorid = models.CharField(db_column='scopusAuthorID', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_scopus_author_mapping'


class UserTotalScore(models.Model):
    user_id = models.IntegerField(primary_key=True)
    online_score = models.IntegerField(blank=True, null=True)
    offline_score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_total_score'


class UsercommentComment(models.Model):
    commentee_user_id = models.IntegerField(blank=True, null=True)
    comment_id = models.IntegerField(blank=True, null=True)
    comment_date = models.DateTimeField(blank=True, null=True)
    field_year = models.CharField(db_column='_year', max_length=4, blank=True, null=True)  # Field renamed because it started with '_'.
    field_time = models.CharField(db_column='_time', max_length=8, blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'usercomment_comment'


class UsercommentCommentTemp(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    comment_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usercomment_comment_temp'


class Usercommentnum(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'usercommentnum'


class UsercommentnumTemp(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'usercommentnum_temp'


class Userentityprofiles(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    entity_id = models.IntegerField(blank=True, null=True)
    relevance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userentityprofiles'


class Userfeedback(models.Model):
    ufb_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    col_id = models.IntegerField()
    rating = models.FloatField()
    ratingtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'userfeedback'


class Userinfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    pass_field = models.CharField(db_column='pass', max_length=400, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    role_id = models.IntegerField()
    lastupdate = models.DateTimeField()
    ispilot = models.IntegerField(blank=True, null=True)
    isbeingupdated = models.IntegerField(blank=True, null=True)
    isrequest = models.IntegerField(blank=True, null=True)
    min_score = models.FloatField(blank=True, null=True)
    location = models.CharField(max_length=400, blank=True, null=True)
    job = models.CharField(max_length=400, blank=True, null=True)
    affiliation = models.CharField(max_length=400, blank=True, null=True)
    website = models.CharField(max_length=400, blank=True, null=True)
    aboutme = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    min_score_date = models.DateTimeField(blank=True, null=True)
    writable = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'userinfo'


class UserinfoCopy(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    pass_field = models.CharField(db_column='pass', max_length=400, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    role_id = models.IntegerField()
    lastupdate = models.DateTimeField()
    ispilot = models.IntegerField(blank=True, null=True)
    isbeingupdated = models.IntegerField(blank=True, null=True)
    isrequest = models.IntegerField(blank=True, null=True)
    min_score = models.FloatField(blank=True, null=True)
    location = models.CharField(max_length=400, blank=True, null=True)
    job = models.CharField(max_length=400, blank=True, null=True)
    affiliation = models.CharField(max_length=400, blank=True, null=True)
    website = models.CharField(max_length=400, blank=True, null=True)
    aboutme = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    min_score_date = models.DateTimeField(blank=True, null=True)
    signedhash = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'userinfo_copy'
        unique_together = (('user_id', 'signedhash'), ('user_id', 'signedhash'),)


class UserinfoExp(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    passcode = models.CharField(max_length=100)
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'userinfo_exp'
        unique_together = (('user_id', 'username', 'passcode', 'created'),)


class UserinfoExpLog(models.Model):
    usl_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    action = models.CharField(max_length=100)
    parameters = models.CharField(max_length=255, blank=True, null=True)
    logtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'userinfo_exp_log'


class UserinfoExpRating(models.Model):
    usr_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    col_id = models.IntegerField()
    field_type = models.CharField(db_column='_type', max_length=255)  # Field renamed because it started with '_'.
    rating = models.FloatField()
    ratingtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'userinfo_exp_rating'


class UserinfoScinet(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    passcode = models.CharField(max_length=100)
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'userinfo_scinet'
        unique_together = (('user_id', 'username', 'passcode', 'created'),)


class UserinfoScinetLog(models.Model):
    usl_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    action = models.CharField(max_length=100)
    parameters = models.CharField(max_length=255, blank=True, null=True)
    logtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'userinfo_scinet_log'


class UserinfoScinetRating(models.Model):
    usr_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    col_id = models.IntegerField()
    field_type = models.CharField(db_column='_type', max_length=255)  # Field renamed because it started with '_'.
    rating = models.FloatField()
    ratingtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'userinfo_scinet_rating'


class Userlikednum(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'userlikednum'


class UserlikednumTemp(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    field_no = models.BigIntegerField(db_column='_no', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'userlikednum_temp'


class Userlikeswhom(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    like_id = models.IntegerField(blank=True, null=True)
    user_who_comments_id = models.IntegerField(blank=True, null=True)
    liketime = models.DateTimeField(blank=True, null=True)
    field_year = models.CharField(db_column='_year', max_length=4, blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'userlikeswhom'


class Usernote(models.Model):
    un_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    col_id = models.IntegerField()
    usernote = models.TextField()
    lastupdate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'usernote'


class Usernotified(models.Model):
    un_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    notified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'usernotified'


class Userprofile(models.Model):
    userprofile_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    col_id = models.IntegerField()
    lastupdate = models.DateTimeField()
    usertags = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    invisible = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'userprofile'
        unique_together = (('user_id', 'col_id'),)


class Usersim(models.Model):
    rec_method_id = models.SmallIntegerField(primary_key=True)
    user0_id = models.IntegerField()
    user1_id = models.IntegerField()
    sim = models.FloatField()
    caltime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'usersim'
        unique_together = (('rec_method_id', 'user0_id', 'user1_id'), ('rec_method_id', 'user0_id', 'user1_id'),)


class Vwcoltermidf(models.Model):
    term = models.CharField(max_length=100, blank=True, null=True)
    ngram = models.IntegerField(blank=True, null=True)
    idf = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vwcoltermidf'


class Vwcoltermtfidf(models.Model):
    col_id = models.IntegerField(blank=True, null=True)
    term = models.CharField(max_length=100, blank=True, null=True)
    ngram = models.IntegerField(blank=True, null=True)
    tfidf = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vwcoltermtfidf'


class Vwlinkedinmapping(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    linkedinid = models.CharField(db_column='linkedinID', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vwlinkedinmapping'



"""  START My Models  """
class Colvideo(models.Model):
    title = models.CharField(max_length=400)
    detail = models.TextField(blank=True, null=True)
    date = models.DateTimeField()  # Field renamed because it started with '_'.
    location = models.CharField(max_length=300)
    url = models.CharField(max_length=400, blank=True, null=True)
    # owner_id = models.IntegerField()
    video_url = models.CharField(max_length=500, blank=True, null=True)
    slide_url = models.CharField(max_length=500, blank=True, null=True)
    paper_url = models.CharField(max_length=500, blank=True, null=True)
    colloquium = models.OneToOneField(Colloquium, on_delete=models.CASCADE, default='')
    user = models.ForeignKey(Userinfo, related_name='colvideos', on_delete=models.CASCADE, default='')
    speaker = models.ForeignKey(Speaker, related_name='colvideos', on_delete=models.CASCADE, default='', null=True)
    s_bio = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'colvideo'


class ColKeywordStr(models.Model):
    keyword_str = models.TextField(blank=True, null=True)
    colvideo = models.OneToOneField(Colvideo, on_delete=models.CASCADE, default='', related_name='keywords_str')

    class Meta:
        db_table = 'col_keyword_str'


#  Colloquium keywords
class ColKeyword(models.Model):
    stem = models.CharField(max_length=45, blank=True, null=True)
    tf = models.IntegerField(blank=True, null=True)
    tfidf = models.FloatField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    is_title = models.IntegerField(blank=True, null=True)
    pos_title = models.TextField(blank=True, null=True)
    pos_detail = models.TextField(blank=True, null=True)
    colvideo = models.ForeignKey(Colvideo, on_delete=models.CASCADE, default='', related_name='keywords')
    # colloquium = models.ForeignKey(Colloquium, on_delete=models.CASCADE, default='')
    
    class Meta:
        db_table = 'col_keyword'


class KeywordPosTitle(models.Model):
    from_pos = models.IntegerField(blank=True, null=True)
    to_pos = models.IntegerField(blank=True, null=True)
    col_kw = models.ForeignKey(ColKeyword, on_delete=models.CASCADE, default='', related_name='positions_title')

    class Meta:
        db_table = 'keyword_pos_title'


class KeywordPosDetail(models.Model):
    from_pos = models.IntegerField(blank=True, null=True)
    to_pos = models.IntegerField(blank=True, null=True)
    col_kw = models.ForeignKey(ColKeyword, on_delete=models.CASCADE, default='', related_name='positions_detail')

    class Meta:
        db_table = 'keyword_pos_detail'


class Keyphrase(models.Model):
    phrase = models.TextField()
    sequence = models.TextField()   # Parse as json later
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'keyphrase'



class GlobalKeyword(models.Model):
    stem = models.CharField(max_length=45, blank=True, null=True)
    term = models.CharField(max_length=45, blank=True, null=True)
    df = models.IntegerField(blank=True, null=True)
    entropy = models.FloatField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    variations = models.TextField()
    num_keyphrases = models.IntegerField(blank=True, null=True)
    keyphrases = models.ManyToManyField(Keyphrase, blank=True, related_name='global_keywords')
    colvideos = models.ManyToManyField(Colvideo)
    class Meta:
        db_table = 'global_keyword'            



# Usertags extracted from userprofiles
class Usertag(models.Model):
    tag = models.CharField(max_length=45, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE, default='')
    #  fix here, keep reference to colloquium , then retrieve colvideo -> colloquium -> usertags
    # colloquium = models.ManyToManyField(Colloquium, related_name='tags')
    colvideos = models.ManyToManyField(Colvideo, related_name='tags')
    proxusertags = models.ManyToManyField('self', blank=True)

    # def get_colvideo_id

    class Meta:
        db_table = 'usertag'


class ColvideoTagStr(models.Model):
    tag_str = models.TextField()
    colvideo = models.OneToOneField(Colvideo, on_delete=models.CASCADE, related_name='tags_str', default='')

    class Meta:
        db_table = 'colvideo_tag_str'



"""  END My Models  """
