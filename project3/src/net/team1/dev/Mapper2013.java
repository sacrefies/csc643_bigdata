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
import java.util.logging.Logger;

/**
 * A mapper class for the 2013 housing data
 */
public class Mapper2013 extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {
    private static final Logger LOG = Logger.getLogger(HousingAnalysis.class.getName());

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
        HashMap<String, Integer> cols = DataPreprocessor.ColumnConfig2013;

        // Housing data come in as lines of comma-separated data
        String row[] = preprocessor.removeQuotes().trimSpaces().getFields(",");
        int region = Integer.parseInt(row[cols.get("Region")]);
        String location = row[cols.get("Location")].contains("-5") ? "Suburban" : "City";
        int age = Integer.parseInt(row[cols.get("Age")]);
        int persons = Integer.parseInt(row[cols.get("Persons")]);
        String ownRent = row[cols.get("RentOwn")];
        double income = (Double.parseDouble(row[cols.get("Income")]) < 0.) ?
                0. : Double.parseDouble(row[cols.get("Income")]);

        //Get the Variables
        int count = 0;
        double rating = 0.;
        //Check for missing data
        if (persons != -6 && age != -9 && !ownRent.contains(".") && income != -9) {
            rating = age % 10 + persons + ((ownRent.contains("own")) ? 1 : 2);
            count = 1;
        }

        Text keyEmitted = new Text(region + ", " + location);
        // count[1 for all data available, 0 for missing data], ratings, Total Wage Income
        Text valueEmitted = new Text(String.format("%1$d,%2$.4f,%3$.2f", count, rating, income));
        outputCollector.collect(keyEmitted, valueEmitted);

        String log = String.format("[(%1$d, %2$s),(%3$d, %4$f, %5$f), orginal: (%6$d, %7$d, %8$s, %5$f)]",
                region, location, count, rating, income, age, persons, ownRent);
        LOG.info(log);
    }
}
