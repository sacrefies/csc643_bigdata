// ----------------------------------------------------------------------------
// Copyright 2017 team1@course_bigdata, Saint Joseph's University
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ----------------------------------------------------------------------------


package net.team1.dev;

import java.util.HashMap;

/**
 * A preprocessor for the input data files.
 */
class DataPreprocessor {
    /**
     * Create and initialize an instance of class DataPreprocessor
     *
     * @param original The original string data to be processed.
     */
    DataPreprocessor(String original) {
        line = original;
    }

    /**
     * Remove both single and double quotes from the data.
     *
     * @return A new DataPreprocessor instance which contains the processed data line.
     */
    DataPreprocessor removeQuotes() {
        return (line == null) ? null : new DataPreprocessor(line = line.replaceAll("\'", "").replaceAll("\"", ""));
    }

    /**
     * Remove all spaces in the data line.
     * @return A new DataPreprocessor instance which contains the processed data line.
     */
    DataPreprocessor trimSpaces() {
        return (line==null)? null: new DataPreprocessor(line = line.replaceAll("\\s", ""));
    }

    /**
     * Split the data line into an array of fields.
     * @param delimiter The separator
     * @return A String array which contains the fields.
     */
    String[] getFields(String delimiter) {
        return (line == null)? null : (delimiter == null) ? new String[] {line}: line.split(delimiter);
    }

    /**
     * @inheritDoc
     */
    @Override
    public String toString() {
        return line;
    }

    /**
     * The processed input line from the input file.
     */
    private String line;

    /**
     * The column/field positions of 2013
     */
    static final HashMap<String, Integer> ColumnConfig2013;
    /**
     * The column/field positions of 2003
     */
    static final HashMap<String, Integer> ColumnConfig2003;
    /**
     * The column/field positions of 2005
     */
    static final HashMap<String, Integer> ColumnConfig2005;
    /**
     * The column/field positions of 2007
     */
    static final HashMap<String, Integer> ColumnConfig2007;
    /**
     * The column/field positions of 2011
     */
    static final HashMap<String, Integer> ColumnConfig2011;

    /**
     * Initialize the static fields before they are used.
     */
    static {
        // init the column configuration of 2013
        ColumnConfig2013 = new HashMap<>();
        ColumnConfig2013.put("Region", 3);
        ColumnConfig2013.put("Age", 1);
        ColumnConfig2013.put("Persons", 20);
        ColumnConfig2013.put("Income", 32);
        ColumnConfig2013.put("Location", 75);
        ColumnConfig2013.put("RentOwn", 79);

        // init the columns configurations from 2003 ~ 2011
        ColumnConfig2003 = new HashMap<>();
        ColumnConfig2003.put("Region", 3);
        ColumnConfig2003.put("Age", 1);
        ColumnConfig2003.put("Persons", 12);
        ColumnConfig2003.put("Income", 26);
        ColumnConfig2003.put("Location", 75);
        ColumnConfig2003.put("RentOwn", 79);

        ColumnConfig2005 = new HashMap<>();
        ColumnConfig2005.put("Region", 4);
        ColumnConfig2005.put("Age", 1);
        ColumnConfig2005.put("Persons", 3);
        ColumnConfig2005.put("Income", 32);
        ColumnConfig2005.put("Location", 75);
        ColumnConfig2005.put("RentOwn", 79);

        ColumnConfig2007 = new HashMap<>();
        ColumnConfig2007.put("Region", 4);
        ColumnConfig2007.put("Age", 1);
        ColumnConfig2007.put("Persons", 3);
        ColumnConfig2007.put("Income", 32);
        ColumnConfig2007.put("Location", 75);
        ColumnConfig2007.put("RentOwn", 79);

        ColumnConfig2011 = new HashMap<>();
        ColumnConfig2011.put("Region", 3);
        ColumnConfig2011.put("Age", 1);
        ColumnConfig2011.put("Persons", 10);
        ColumnConfig2011.put("Income", 32);
        ColumnConfig2011.put("Location", 75);
        ColumnConfig2011.put("RentOwn", 79);
    }
}
