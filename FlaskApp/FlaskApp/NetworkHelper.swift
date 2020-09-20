//
//  NetworkHelper.swift
//  FlaskApp
//
//  Created by Sue Cho on 2020/09/19.
//  Copyright © 2020 Sue Cho. All rights reserved.
//

import Foundation

struct TestObject: Codable {
    var numberOfFields: Int?
    var result: String?
}

// Singleton Instance for Network
class NetworkHelper {
    
    static var shared = NetworkHelper()
    private let baseURL = "http://127.0.0.1:5000/entry"
    
    private init() { }
    
    func getData(numberOfFields: Int, result: String, completion: @escaping (TestObject) -> Void) {
        // Create Session
        let defaultSession = URLSession(configuration: .default)
        guard let url = URL(string: "\(baseURL)") else {
            return // URL = nil
        }
        
        // Request
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        let dict = ["numberOfFields" : numberOfFields, "result" : result] as [String : Any]
        guard let jsonData = try? JSONSerialization.data(withJSONObject: dict, options: []) else {
            return // jsonData filaed to serialize
        }
        request.httpBody = jsonData
        
        // data task
        let dataTask = defaultSession.dataTask(with: request) { (data: Data?, response: URLResponse?, error: Error?) in
            // data error
            guard error == nil else {
                return
            }
            guard let data = data, let response = response as? HTTPURLResponse, response.statusCode == 200 else {
                return
            }
            
            let decoder = JSONDecoder()
            guard let testObject = try? decoder.decode(TestObject.self, from: data) else {
                return
            }
            
            completion(testObject)
        }
        dataTask.resume()
    }
    
}
