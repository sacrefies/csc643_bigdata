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

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;

import java.io.IOException;
import java.util.Iterator;
import java.util.logging.Logger;

/**
 * A reducer class for the 2013 housing data
 */
public class HousingReducer extends MapReduceBase implements Reducer<Text, Text, Text, Text> {
    private static final Logger LOG = Logger.getLogger(HousingAnalysis.class.getName());

    /**
     * A reduce function to aggregate the mapped data.
     *
     * @param key             The input key
     * @param values          The input value
     * @param outputCollector The output key/value pair collector
     * @param reporter        The reporter
     * @throws IOException When the input stream is invalid.
     */
    @Override
    public void reduce(Text key, Iterator<Text> values,
                       OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {
        int totalCount = 0;
		int incomeCount = 0; 
        double ratingSum = 0.;
        double incomeSum = 0.;
        while (values.hasNext()) {
            String tokens[] = values.next().toString().split(",");
            totalCount += Integer.parseInt(tokens[0]);
            ratingSum += Double.parseDouble(tokens[1]);
			if(Double.parseDouble(tokens[1] != 0)) {
				incomeSum += Double.parseDouble(tokens[2]);
				incomeCount ++; 
			}
            String log = String.format("(%1$s), (%2$d, %3$f, %4$f)", key.toString(),
                    Integer.parseInt(tokens[0]), Double.parseDouble(tokens[1]), Double.parseDouble(tokens[2]));
            LOG.info(log);
        }
        LOG.info(String.format("(%1$s), (%2$d, %3$f, %4$f)", key.toString(), totalCount, ratingSum, incomeSum));
        Text value = new Text(String.format("%1$d,%2$.4f,%3$.2f", totalCount, ratingSum / totalCount, incomeSum / incomeCount));
        outputCollector.collect(key, value);
    }
}
