import pandas as pd
from qordoba.settings import get_localization_files
from qordoba.commands.i18n_base import BaseClass, FilesNotFound
import logging
log = logging.getLogger('qordoba')

existing_i18n_KEY_VALUES = dict()

class FindNewConverter(BaseClass):

    def get_existing_i18n_key_values(self, config):
        # greps localization file from config and stores all the key value pairs within existing_i18n_KEY_VALUES
        localization_files = get_localization_files(config)
        for file in localization_files:
            dictionary = self.get_nested_dictionary(file)
            key_values = self.get_all_keys(dictionary, list(), dict())
            existing_i18n_KEY_VALUES[file] = key_values
            return existing_i18n_KEY_VALUES

    def index_lookup(self, stringLiteral):
        # checks if stringLiteral exists in values, gives back corresponding key or None
        for i18n_file in existing_i18n_KEY_VALUES:
            for key, value in existing_i18n_KEY_VALUES[i18n_file].items():

                if value.encode('UTF-8') == stringLiteral:
                    return key

        return None


    def get_key_of_StringLiterals(self, config, filepath):

        # loading CSV into dataframe
        column_names = ['filename', 'startLineNumber', 'startCharIdx', 'endLineNumber', 'endCharIdx', 'text']
        df = pd.read_csv(filepath, header=None, names=column_names)

        # getting existing key value pairs from localization files
        self.get_existing_i18n_key_values(config)

        # lookup if Stringliteral exists as value in localization file. If yes, return key, otherwise None.
        # adding new key column to Dataframe
        df['key'] = df['text'].apply(lambda x: self.index_lookup(x))

        log.info("StringLiterals  were matched to existing keys. Results: ")
        print(df.text)
        print(df.key)

        return df

#
# file = '../../resources/stringLiterals/python_string_literals.csv'
# FindNewConverter().get_key_of_StringLiterals(None, file)
