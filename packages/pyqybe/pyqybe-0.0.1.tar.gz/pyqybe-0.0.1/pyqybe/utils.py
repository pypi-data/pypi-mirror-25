import re


class QueryUtils:
    def clean_query(self, query):
        query = self.remove_sql_commentaries(query)
        return self.remove_duplicate_spaces(self.remove_line_and_tabs(query))

    @staticmethod
    def remove_sql_commentaries(query):
        query = re.sub(re.compile("--.*?\n"), "",
                       query)  # remove all occurance singleline comments (//COMMENT\n ) from query
        return query

    @staticmethod
    def remove_line_and_tabs(string):
        return string.replace('\n', ' ').replace('\t', ' ').strip()

    @staticmethod
    def remove_duplicate_spaces(string):
        return re.sub(' +', ' ', string)


def clean_query(query):
    return QueryUtils().clean_query(query)
