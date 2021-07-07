/*******************************************************************************
 * Copyright 2017 Cognizant Technology Solutions
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License.  You may obtain a copy
 * of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
 * License for the specific language governing permissions and limitations under
 * the License.
 ******************************************************************************/
package com.cognizant.devops.platformregressiontest.test.ui.serverconfiguration;

import java.io.File;
import java.util.concurrent.TimeUnit;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

import com.cognizant.devops.platformregressiontest.test.common.ConfigOptionsTest;
import com.cognizant.devops.platformregressiontest.test.common.LoginAndSelectModule;

/**
 * @author NivethethaS
 * 
 *         Class contains the test cases for server configuration roles test
 *         cases
 *
 */
public class ServerConfigurationTest extends LoginAndSelectModule {

	private static final Logger log = LogManager.getLogger(ServerConfigurationTest.class);

	ServerConfiguration clickAllActionButton;

	String line = "============================================================================================================================================================";

	/**
	 * This method will be run before any test method belonging to the classes
	 * inside the <test> tag is run.
	 * 
	 * @throws InterruptedException
	 */
	@BeforeTest
	public void setUp() {
		initialization();
		getData(ConfigOptionsTest.SERVERCONFIGURATION_DIR + File.separator + ConfigOptionsTest.SERVERCONFIGURATION_JSON_FILE);
		selectModuleUnderConfiguration(LoginAndSelectModule.testData.get("serverconf"));
		clickAllActionButton = new ServerConfiguration();
	}

	/**
	 * This method will be executed just before any function/method with @Test
	 * annotation starts.
	 */
	@BeforeMethod
	public void beforeMethod() {
		driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
	}

	/**
	 * Assert true if landing page is displayed else false
	 */
	@Test(priority = 1)
	public void navigateToServerConfigurationLandingPage() {
		log.info(line);
		Assert.assertTrue(clickAllActionButton.navigateToServerConfigurationLandingPage(),
				"Bulk upload Landing page is displayed");
	}
	
	/**
	 * Assert true if redirect functionality successful else false
	 * 
	 * @throws InterruptedException
	 */
	@Test(priority = 2)
	public void checkRedirectFunctionality() {
		log.info(line);
		Assert.assertTrue(clickAllActionButton.redirectFunctionality(),
				"redirect functionality successful");
	}
	
	/**
	 * Assert true if save button functionality successful else false
	 * 
	 * @throws InterruptedException
	 */
	@Test(priority = 3)
	public void chackSaveButton() {
		log.info(line);
		selectModuleUnderConfiguration(LoginAndSelectModule.testData.get("serverconf"));
		Assert.assertTrue(clickAllActionButton.saveConfiguration(),
				"save button functionality successful");
	}

	/**
	 * This method will be executed just after any function/method with @Test
	 * annotation ends.
	 */
	@AfterMethod
	public void afterMethod() {
		log.info(line);
	}
}
