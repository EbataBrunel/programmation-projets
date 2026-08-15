package eajc.group.apv.services;

import eajc.group.apv.dto.RecaptchaResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Service
public class CaptchaServiceImpl implements  CaptchaService{

    @Value("${google.recaptcha.secret}")
    private String secret;


    private final RestTemplate restTemplate =
            new RestTemplate();


    @Override
    public boolean verifyCaptcha(String token) {
        String url =
                "https://www.google.com/recaptcha/api/siteverify";


        UriComponentsBuilder builder =
                UriComponentsBuilder
                        .fromHttpUrl(url)
                        .queryParam("secret", secret)
                        .queryParam("response", token);



        RecaptchaResponse response =
                restTemplate.postForObject(
                        builder.toUriString(),
                        null,
                        RecaptchaResponse.class
                );


        return response != null
                && response.isSuccess();
    }
}
