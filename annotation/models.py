# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

@python_2_unicode_compatible
class Label(models.Model):
    label = models.CharField(max_length=100)
    option = models.CharField(max_length=5)
    #
    def __str__(self):
        return self.label


@python_2_unicode_compatible
class Document(models.Model):
    document = models.CharField(max_length=10000)
    doc_id = models.CharField(max_length=1000)
    preprocessed = models.CharField(max_length=10000)
    trainInstance = models.BooleanField()
    active_prediction = models.ForeignKey(Label, null=True, blank=True)
    margin = models.FloatField(default=1.0)
    #
    def __str__(self):
        return self.document[:100]


@python_2_unicode_compatible
class AnnotationQueue(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    max_anno_num = models.IntegerField(default=0)
    def __str__(self):
        user = 'User: ' + self.user.__str__()
        elements = ' '.join(map(lambda e: e.__str__(),
                                QueueElement.objects.filter(queue=self)))
        return user + '  (rank/doc_pk/proposal): ' + elements


@python_2_unicode_compatible
class QueueElement(models.Model):
    document = models.ForeignKey(Document,
                                 on_delete=models.CASCADE)
    queue = models.ForeignKey(AnnotationQueue)
    proposalFlag = models.CharField(max_length=15, default='no proposal')
    rank = models.IntegerField(default=0)
    def __str__(self):
        doc = str(self.document.pk)
        proposal = self.proposalFlag
        rank = str(self.rank)
        return rank + '/' + doc + '/' + proposal + ','


@python_2_unicode_compatible
class Score(models.Model):
    document = models.ForeignKey(Document,
                                 on_delete=models.CASCADE)
    label = models.ForeignKey(Label,
                              on_delete=models.CASCADE)
    nbc_normalized = models.FloatField(default=0.0)
    nbc_prior = models.FloatField(default=0.0)
    nbc_term_given_label = models.FloatField(default=0.0)
    nbc_total = models.FloatField(default=0.0)
    def __str__(self):
        l = self.label.__str__() + ' '
        d = ''#self.document.__str__() + ' '
        n = str(self.nbc_normalized) + ' '
        p = str(self.nbc_prior) + ' '
        tgl = str(self.nbc_term_given_label) + ' '
        t = str(self.nbc_total)
        return l+d+n+p+tgl+t


@python_2_unicode_compatible
class Annotation(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    labels = models.ManyToManyField(Label)
    proposals = models.ManyToManyField(Label, related_name='proposals')
    duration = models.CharField(max_length=100)
    dateTime =  models.DateTimeField(auto_now_add=True)
    #
    def __str__(self):
        user = 'User: ' + self.user.__str__()
        duration = ', duration: ' + str(round(float(self.duration)/100)/10) + ' secs, '
        dateTime = 'on ' + self.dateTime.strftime("%Y-%m-%d %H:%M:%S") + ', '
        labels = 'labels: ' + ', '.join([l.label for l in self.labels.all()]) + ', '
        proposals = 'proposals: ' + ', '.join([p.label for p in self.proposals.all()])
        docs = ', doc: ' + self.document.__str__().decode('utf-8')
        return user + duration + dateTime + labels + proposals + docs


@python_2_unicode_compatible
class NBC_class_count(models.Model):
    label = models.ForeignKey(Label)
    count = models.IntegerField()
    total_word_count = models.IntegerField()
    #
    def __str__(self):
        count = 'Class count: ' + str(self.count)
        label = ' of label: ' + self.label.__str__()
        words = ' with a total of ' + str(self.total_word_count) + ' words'
        return count + label + words


@python_2_unicode_compatible
class NBC_vocabulary(models.Model):
    word = models.CharField(max_length=100)
    #
    def __str__(self):
        return self.word


@python_2_unicode_compatible
class NBC_word_count_given_class(models.Model):
    label = models.ForeignKey(Label)
    word = models.ForeignKey(NBC_vocabulary) # models.CharField(max_length=100)
    count = models.IntegerField()
    def __str__(self):
        w = '"' + self.word.__str__() + '"' + ' occured '
        c = str(self.count) + ' times in class '
        return w + c + self.label.__str__()
