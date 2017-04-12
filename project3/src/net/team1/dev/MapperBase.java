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

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

import java.io.IOException;
import java.util.HashMap;

/**
 * A base class for all the mappers.
 */
public abstract class MapperBase extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {
    /**
     * A map function to map the data.
     *
     * @param longWritable    The input data stream identifier
     * @param value           the input value
     * @param outputCollector The emitted key/value pair collector.
     * @param reporter        The reporter
     * @throws IOException When the input data stream is invalid.
     */
    @Override
    public void map(LongWritable longWritable, Text value,
                    OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {
        DataPreprocessor preprocessor = new DataPreprocessor(value.toString());
        // Housing data come in as lines of comma-separated data
        String row[] = preprocessor.removeQuotes().trimSpaces().getFields(",");

        int age = Integer.parseInt(row[columns.get("Age")]);
        // age == -9 means it's invalid. No emission
        if (age == DataPreprocessor.INVALID_INDENTIFIER) return;

        int region = Integer.parseInt(row[columns.get("Region")]);
        String location = row[columns.get("Location")].contains("-5") ? "Suburban" : "City";
        int persons = (Integer.parseInt(row[columns.get("Persons")]) < 1) ?
                0 : Integer.parseInt(row[columns.get("Persons")]);
        String ownRent = row[columns.get("RentOwn")].toLowerCase();
        double income = (Double.parseDouble(row[columns.get("Income")]) < 0.) ?
                0. : Double.parseDouble(row[columns.get("Income")]);

        double rating = age % 10 + persons + ((ownRent.contains("own")) ? 1 : 2);
        int count = 1;

        Text keyToEmit = new Text(region + ", " + location + ", " + year);
        // count[1 for all data available, 0 for missing data], ratings, Total Wage Income
        Text valueToEmit = new Text(String.format("%1$d,%2$.4f,%3$.2f", count, rating, income));
        outputCollector.collect(keyToEmit, valueToEmit);
    }

    /**
     * Set up the configurations for the input data respectively.
     *
     * @param columnConfig The fields configuration
     * @param whichYear    For which year the input data is
     */
    protected void setUp(HashMap<String, Integer> columnConfig, int whichYear) {
        columns = columnConfig;
        year = whichYear;
    }

    /**
     * The data field configuration
     */
    private HashMap<String, Integer> columns;

    /**
     * For which year the data is.
     */
    private int year = 0;
}
