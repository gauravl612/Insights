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
package com.cognizant.devops.platformservice.customsettings;

import java.util.Base64;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.cognizant.devops.platformcommons.config.ApplicationConfigProvider;
import com.cognizant.devops.platformdal.icon.Icon;
import com.cognizant.devops.platformdal.icon.IconDAL;
import com.cognizant.devops.platformservice.rest.util.PlatformServiceUtil;
import com.google.gson.JsonObject;

@RestController
@RequestMapping("/settings")
public class CustomAppSettings {

	private static Logger log = LogManager.getLogger(CustomAppSettings.class);

    @CrossOrigin
	@GetMapping(value = "/getLogoImage" )
	public @ResponseBody JsonObject getImageWithMediaType() {
    	String base64 = "";
		String imageType = "";
		ImageResponse imgResp = new ImageResponse();
		try {
			if(ApplicationConfigProvider.getInstance().getPostgre().getUserName()!=null 
					&& !ApplicationConfigProvider.getInstance().getPostgre().getUserName().equals("")) {
				Icon image = new IconDAL().fetchEntityData("logo");
				if (null != image.getImageType()) {
					imageType = image.getImageType();
				}
				if (null != image.getImage()) {
					byte[] imageBytes = image.getImage();
					base64 = Base64.getEncoder().encodeToString(imageBytes);
				}
			}
			imgResp.setEncodedString(base64);
			imgResp.setImageType(imageType);
			return PlatformServiceUtil.buildSuccessResponseWithData(imgResp);
		} catch (Exception e) {
			log.error(e);
			log.error(" Unable to fetch image information  ",e);
			return PlatformServiceUtil.buildSuccessResponseWithData(imgResp);
		}
	}
}
