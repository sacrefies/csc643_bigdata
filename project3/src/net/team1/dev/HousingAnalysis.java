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

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;

import java.io.IOException;
import java.util.Iterator;


/**
 * A class for the map/reduce process
 */
public class HousingAnalysis {

    /**
     * An inner class to set-up the mapper function.
     */
    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {
        /**
         * A map function to map the data.
         *
         * @param key      The input key
         * @param value    the input value
         * @param output   The output key
         * @param reporter The output value
         * @throws IOException When the input data stream is invalid.
         */
        public void map(LongWritable key, Text value, OutputCollector<Text, Text> output, Reporter reporter) throws IOException {
            // Housing data come in as lines of comma-separated data
            String row[] = value.toString().split(",");
            int region = Integer.parseInt(row[3]);
            String location = row[75].contains("-5") ? "Suburban" : "City";
            int age = Integer.parseInt(row[1]);
            int persons = Integer.parseInt(row[20]);
            String ownRent = row[79];
            double income = (Double.parseDouble(row[32]) < 0.) ? 0. : Double.parseDouble(row[32]);

            //Get the Variables
            int count = 0;
            double rating = 0.;
            //Check for missing data
            if (persons != -6 && age != -9 && !ownRent.contains(".") && income != -9) {
                rating = age % 10 + persons + ((ownRent.contains("own")) ? 1 : 2);
                count = 1;
            }

            Text mappedKey = new Text();
            Text variables = new Text();

            mappedKey.set(region + "," + location);
            // count[1 for all data available, 0 for missing data], ratings, Total Wage Income
            variables.set(count + "," + Double.toString(rating) + "," + Double.toString(income));
            output.collect(mappedKey, variables);
        }
    }

    /**
     * An inner class to set-up the reduce function
     */
    public static class Reduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {
        /**
         * A reduce function to aggregate the mapped data.
         *
         * @param key      The input key
         * @param values   The input value
         * @param output   The output key
         * @param reporter The output value
         * @throws IOException When the input stream is invalid.
         */
        public void reduce(Text key, Iterator<Text> values, OutputCollector<Text, Text> output, Reporter reporter) throws IOException {
            int totalCount = 0;
            double ratingSum = 0;
            double incomeSum = 0;

            while (values.hasNext()) {
                String tokens[] = values.next().toString().split(",");
                totalCount += Integer.parseInt(tokens[0]);
                ratingSum += Double.parseDouble(tokens[1]);
                incomeSum += Double.parseDouble(tokens[2]);
            }
            output.collect(key, new Text(totalCount + "," + (ratingSum / totalCount) + "," + (incomeSum / totalCount)));
        }
    }


    //**************************************************************************
    public static void main(String[] args) throws Exception {
        JobConf conf = new JobConf(HousingAnalysis.class);
        conf.setJobName("housinganalysis");

        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(Text.class);

        conf.setMapperClass(Map.class);
        conf.setCombinerClass(Reduce.class);
        conf.setReducerClass(Reduce.class);

        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);

        FileInputFormat.setInputPaths(conf, new Path(args[0]));
        FileOutputFormat.setOutputPath(conf, new Path(args[1]));

        JobClient.runJob(conf);
    }
}


