//
//  PieChartView.swift
//  FlaskApp
//
//  Created by Sue Cho on 2020/09/19.
//  Copyright © 2020 Sue Cho. All rights reserved.
//

import os.log
import UIKit

struct Slice {
    var percent: CGFloat
    var color: UIColor
}

class PieChartView: UIView {
    
    static let ANIMATION_DURATION: CGFloat = 1.4
    
    @IBOutlet var canvasView: UIView!
    
    @IBOutlet var label1: UILabel!
    @IBOutlet var label2: UILabel!
    @IBOutlet var label3: UILabel!
    @IBOutlet var label4: UILabel!
    @IBOutlet var label5: UILabel!
    
    @IBOutlet var label1XConst: NSLayoutConstraint!
    @IBOutlet var label2XConst: NSLayoutConstraint!
    @IBOutlet var label3XConst: NSLayoutConstraint!
    @IBOutlet var label4XConst: NSLayoutConstraint!
    @IBOutlet var label5XConst: NSLayoutConstraint!

    @IBOutlet var label1YConst: NSLayoutConstraint!
    @IBOutlet var label2YConst: NSLayoutConstraint!
    @IBOutlet var label3YConst: NSLayoutConstraint!
    @IBOutlet var label4YConst: NSLayoutConstraint!
    @IBOutlet var label5YConst: NSLayoutConstraint!
    
    var slices: [Slice]?
    var sliceIndex: Int = 0
    var currentPercent: CGFloat = 0.0
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        let view: UIView = Bundle.main.loadNibNamed("PieChartView", owner: self, options: nil)!.first as! UIView
        addSubview(view)
    }

    override func draw(_ rect: CGRect) {
        subviews[0].frame = bounds
    }

    func getDuration(_ slice: Slice) -> CFTimeInterval {
        return CFTimeInterval(slice.percent / 1.0 * PieChartView.ANIMATION_DURATION)
    }
    
    func percentToRadian(_ percent: CGFloat) -> CGFloat {
        //Because angle starts wtih X positive axis, add 270 degrees to rotate it to Y positive axis.
        var angle = 270 + percent * 360
        if angle >= 360 {
            angle -= 360
        }
        return angle * CGFloat.pi / 180.0
    }

    func addSlice(_ slice: Slice) {
        let animation = CABasicAnimation(keyPath: "strokeEnd")
        animation.fromValue = 0
        animation.toValue = 1
        animation.duration = getDuration(slice)
        animation.timingFunction = CAMediaTimingFunction(name: CAMediaTimingFunctionName.linear)
        animation.delegate = self
        
        let canvasWidth = canvasView.frame.width
        let path = UIBezierPath(arcCenter: canvasView.center,
                                radius: canvasWidth * 3 / 8,
                                startAngle: percentToRadian(currentPercent),
                                endAngle: percentToRadian(currentPercent + slice.percent),
                                clockwise: true)
        
        let sliceLayer = CAShapeLayer()
        sliceLayer.path = path.cgPath
        sliceLayer.fillColor = nil
        sliceLayer.strokeColor = slice.color.cgColor
        sliceLayer.lineWidth = canvasWidth * 2 / 8
        sliceLayer.strokeEnd = 1
        sliceLayer.add(animation, forKey: animation.keyPath)
        
        canvasView.layer.addSublayer(sliceLayer)
    }
    
    func getLabelCenter(_ fromPercent: CGFloat, _ toPercent: CGFloat) -> CGPoint {
        let radius = canvasView.frame.width * 3 / 8
        let labelAngle = percentToRadian((toPercent - fromPercent) / 2 + fromPercent)
        let path = UIBezierPath(arcCenter: canvasView.center,
                                radius: radius,
                                startAngle: labelAngle,
                                endAngle: labelAngle,
                                clockwise: true)
        path.close()
        return path.currentPoint
    }
    

    func addLabel(_ slice: Slice) {
        let center = canvasView.center
        let labelCenter = getLabelCenter(currentPercent, currentPercent + slice.percent)
        let xConst = [label1XConst, label2XConst, label3XConst, label4XConst, label5XConst][sliceIndex]
        let yConst = [label1YConst, label2YConst, label3YConst, label4YConst, label5YConst][sliceIndex]
        xConst?.constant = labelCenter.x - center.x
        yConst?.constant = labelCenter.y - center.y
        canvasView.superview?.setNeedsUpdateConstraints()
        canvasView.superview?.layoutIfNeeded()

        let label = [label1, label2, label3, label4, label5][sliceIndex]
        label?.isHidden = true
        label?.text = String(format: "%d%%", Int(slice.percent * 100))
    }
    
    func animateChart() {
        sliceIndex = 0
        currentPercent = 0.0
        canvasView.layer.sublayers = nil
        
        if slices != nil && slices!.count > 0 {
            let firstSlice = slices![0]
            addLabel(firstSlice)
            addSlice(firstSlice)
        }
    }
}

extension PieChartView: CAAnimationDelegate {
    func animationDidStop(_ anim: CAAnimation, finished flag: Bool) {
        if flag {
            currentPercent += slices![sliceIndex].percent
            sliceIndex += 1
            if sliceIndex < slices!.count {
                let nextSlice = slices![sliceIndex]
                addLabel(nextSlice)
                addSlice(nextSlice)
            } else {
                //After animation is done, display all labels. Can be animated.
                for label in [label1, label2, label3, label4, label5] {
                    label?.isHidden = false
                }
            }
        }
    }
}
